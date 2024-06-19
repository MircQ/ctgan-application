from ctgan import CTGAN, TVAE
from pandas import DataFrame


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

    def generate(self, samples: int) -> DataFrame:

        """
        Generate samples samples using the current model.

        :param int samples: number of samples to generate.
        :return:
        """

        assert self.model is not None

        synthetic_data = self.model.sample(n=samples)

        return synthetic_data
