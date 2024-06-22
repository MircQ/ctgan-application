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

    training_data: pd.DataFrame | None = None

    def train(self, model: str, data: DataFrame):

        # TODO validate data
        # Continuous data must be represented as floats
        # Discrete data must be represented as ints or strings
        # The data should not contain any missing values

        print(f"Starting training function: model {model}")

        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(data=data)

        match model:

            case "CTGAN":
                self.synthesizer = CTGANSynthesizer(metadata=metadata, epochs=3)
            case "TVAE":
                self.synthesizer = TVAESynthesizer(metadata=metadata, epochs=10)
            case _:
                raise Exception

        self.synthesizer.fit(data=data)
        print("Training completed")

        print("End of training function")

    def generate(self, samples: int) -> DataFrame:

        """
        Generate samples samples using the current model.

        :param int samples: number of samples to generate.
        :return: generated samples according to the previously trained model.
        :rtype: pd.Dataframe
        """

        print(f"Starting generating function: n_samples: {samples}")

        assert self.synthesizer is not None

        synthetic_data = self.synthesizer.sample(num_rows=samples)

        print(f"Generation completed")

        print(synthetic_data)

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

        return PDFManager.create_pdf(text=recap, image=fig.to_image(format="png", width=700, height=400))
