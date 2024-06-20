from ctgan import CTGAN, TVAE
from pandas import DataFrame
from sdv.evaluation.single_table import evaluate_quality
from sdv.evaluation.single_table import get_column_plot
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata

class ModelService:

    model: CTGAN | TVAE = None

    discrete_columns: list[str] = [
        'workclass',
        'education',
        'marital-status',
        'occupation',
        'relationship',
        'race',
        'sex',
        'native-country',
        'income'
    ]

    def train(self, model: str, data: DataFrame):

        # TODO validate data
        # Continuous data must be represented as floats
        # Discrete data must be represented as ints or strings
        # The data should not contain any missing values

        match model:

            case "CTGAN":
                model = CTGAN(epochs=10)
            case "TVAE":
                model = TVAE(epochs=10)
            case _:

                raise Exception

        model.fit(train_data=data, discrete_columns=self.discrete_columns)

        # or
        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(data=data)
        synthesizer = CTGANSynthesizer(metadata)
        synthesizer.fit(data=data)

    def generate(self, samples: int) -> DataFrame:

        """
        Generate samples samples using the current model.

        :param int samples: number of samples to generate.
        :return:
        """

        assert self.model is not None

        synthetic_data = self.model.sample(n=samples)

        # or
        # synthetic_data = synthesizer.sample(num_rows=10)

        return synthetic_data

    def evaluate(self, real_data, synthetic_data, metadata):

        quality_report = evaluate_quality(
            real_data,
            synthetic_data,
            metadata)



        fig = get_column_plot(
            real_data=real_data,
            synthetic_data=synthetic_data,
            column_name='amenities_fee',
            metadata=metadata
        )

        fig.show()
