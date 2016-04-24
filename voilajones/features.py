class Feature(object):
    def __init__(self, position, width, height, threshold, polarity):
        self.position = position
        self.tl = position
        self.br = (position[0] + width, position[1] + height)
        self.w = width
        self.h = height
        self.threshold = threshold
        self.polarity = polarity

    def get_vote(self, intImage):
        score = self.get_score(intImage)
        return 1 if score < self.polarity * self.threshold else -1


class FeatureTwoVertical(Feature):
    dimen = (1, 2)

    def get_score(self, intImage):
        first = intImage.get_area_sum(
            self.tl, (self.tl[0] +
                      self.w, self.tl[1] + self.h / 2))

        second = intImage.get_area_sum(
            (self.tl[0], self.tl[1] +
             self.h / 2), self.br)

        score = first - second
        return score


class FeatureTwoHorizontal(Feature):
    dimen = (2, 1)

    def get_score(self, intImage):
        first = intImage.get_area_sum(self.tl, (self.tl[0] + self.w / 2, self.tl[1] + self.h))
        second = intImage.get_area_sum((self.tl[0] + self.w / 2, self.tl[1]), self.br)
        score = first - second
        return score


class FeatureThreeHorizontal(Feature):
    dimen = (3, 1)

    def get_score(self, intImage):
        first = intImage.get_area_sum(self.tl, (self.tl[0] + self.w / 3, self.tl[1] + self.h))
        second = intImage.get_area_sum((self.tl[0] + self.w / 3, self.tl[1]), (self.tl[0] + 2 * self.w / 3, self.tl[1] + self.h))
        third = intImage.get_area_sum((self.tl[0] + 2 * self.w / 3, self.tl[1]), self.br)
        score = first - second + third
        return score


class FeatureTheeVertical(Feature):
    dimen = (1, 3)

    def get_score(self, intImage):
        first = intImage.get_area_sum(self.tl, (self.br[0], self.tl[1] + self.h / 3))
        second = intImage.get_area_sum((self.tl[0], self.tl[1] + self.h / 3), (self.br[0], self.tl[1] + 2 * self.h / 3))
        third = intImage.get_area_sum((self.tl[0], self.tl[1] + 2 * self.h / 3), self.br)
        score = first - second + third
        return score


class FeatureFour(Feature):
    dimen = (2, 2)

    def get_score(self, intImage):
        first = intImage.get_area_sum(self.tl, (self.tl[0] + self.w / 2, self.tl[1] + self.h / 2))
        # top right area
        second = intImage.get_area_sum((self.tl[0] + self.w / 2, self.tl[1]), (self.br[0], self.tl[1] + self.h / 2))
        # bottom left area
        third = intImage.get_area_sum((self.tl[0], self.tl[1] + self.h / 2), (self.tl[0] + self.w / 2, self.br[1]))
        # bottom right area
        fourth = intImage.get_area_sum((self.tl[0] + self.w / 2, self.tl[1] + self.h / 2), self.br)
        score = first - second - third + fourth
        return score


class FEATURE_TYPES:
    TYPE_TWO_VERTICAL = FeatureTwoVertical
    TYPE_TWO_HORIZONTAL = FeatureTwoHorizontal
    TYPE_THREE_HORIZONTAL = FeatureThreeHorizontal
    TYPE_THREE_VERTICAL = FeatureTheeVertical
    TYPE_FOUR_HORIZONTAL = FeatureFour

    ALL = [TYPE_TWO_VERTICAL, TYPE_TWO_HORIZONTAL, TYPE_THREE_HORIZONTAL,
           TYPE_THREE_VERTICAL, TYPE_FOUR_HORIZONTAL]