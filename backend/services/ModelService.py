import logging
from typing import Literal

from pandas import DataFrame
from sdv.evaluation.single_table import evaluate_quality
from sdv.evaluation.single_table import get_column_plot
from sdv.single_table import CTGANSynthesizer, TVAESynthesizer
from sdv.metadata import SingleTableMetadata
from utils.PDFManager import PDFManager
from utils.Singleton import Singleton
import pandas as pd


class ModelService(metaclass=Singleton):

    # This variable will store the last trained model.
    synthesizer: CTGANSynthesizer | TVAESynthesizer | None = None

    # This variable will store the last 
    metadata: SingleTableMetadata | None = None

    def train(self, model: Literal["CTGAN", "TVAE"], data: DataFrame):

        """
        Train the model with the given data.

        :param str model: model name. One between CTGAN and TVAE.
        :param DataFrame data: data on which the model will be trained.
        """

        logging.info(f"Starting training function: model {model}")

        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(data=data)

        match model:

            case "CTGAN":
                self.synthesizer = CTGANSynthesizer(metadata=metadata, epochs=5)
            case "TVAE":
                self.synthesizer = TVAESynthesizer(metadata=metadata, epochs=5)
            case _:
                raise Exception

        self.synthesizer.fit(data=data)
        logging.info("Training completed")


    def generate(self, samples: int) -> DataFrame:

        """
        Generate samples samples using the current model.

        :param int samples: number of samples to generate.
        :return: generated samples according to the previously trained model.
        :rtype: pd.Dataframe
        """

        logging.info(f"Starting generating function: n_samples: {samples}")

        assert self.synthesizer is not None

        synthetic_data = self.synthesizer.sample(num_rows=samples)

        logging.info(f"Generation completed")

        return synthetic_data

    def evaluate(self, column_name: str, real_data: DataFrame, synthetic_data: DataFrame) -> bytes:

        """
        Evaluate the given synthetic_data against the real data.


        :return: raw pdf file containing evaluation scores and images.
        :rtype: bytes
        """

        assert list(synthetic_data.columns) == list(real_data.columns)
        assert column_name in synthetic_data.columns

        real_data = pd.read_csv("adult.csv")
        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(data=real_data)

        logging.info(f"Starting evaluation process: columnn {column_name}")

        quality_report = evaluate_quality(
            real_data=real_data,
            synthetic_data=synthetic_data,
            metadata=metadata,
            verbose=False
        )

        recap = "Overall Score (Average): {0}\nColumn Shapes Score: {1}\nColumn Pair Trends Score: {2}".format(
            quality_report.get_score(),
            quality_report.get_properties().Score[0],
            quality_report.get_properties().Score[1]
        )

        fig = get_column_plot(
            real_data=real_data,
            synthetic_data=synthetic_data,
            column_name=column_name,
            metadata=metadata
        )

        pdf_bytes = PDFManager.create_pdf(text=recap, image=fig.to_image(format="png", width=700, height=400))

        logging.info(f"Evaluation process completed.")

        return pdf_bytes
