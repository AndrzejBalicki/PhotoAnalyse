import config


class Scorer:

    def compute(self, metrics):

        score = 0

        for key, value in metrics.items():

            if value is None:
                print(f"⚠ {key} returned None → ustawiam 0")
                value = 0

            score += config.WEIGHTS[key] * value

        return score