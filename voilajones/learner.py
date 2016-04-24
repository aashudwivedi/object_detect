import numpy as np
import features as ft
import sys


class AdaBoostLearner():
    def __init__(self, image_height, image_width):
        self.features = []

        for feat in ft.FEATURE_TYPES.ALL:
            for width in range(feat.dimen[0], image_width, feat.dimen[0]):
                for height in range(feat.dimen[1], image_height, feat.dimen[1]):
                    for x in range(image_width - width):
                        for y in range(image_height - height):
                            self.features.append(
                                feat((x, y), width, height, 0, 1))

    def addEvidence(self, positives, negatives, bag_count):
        pos_weight = 1. / (2 * len(positives))
        neg_weight = 1. / (2 * len(negatives))

        for p in positives:
            p.set_weight(pos_weight)
        for n in negatives:
            n.set_weight(neg_weight)

        # create column vector
        images = np.hstack((positives, negatives))

        votes = dict()
        i = 0
        for feature in self.features:
            # calculate score for each image, also associate the image
            feature_votes = np.array(map(lambda im: [im, feature.get_vote(im)], images))
            votes[feature] = feature_votes
            i += 1
            if i % 1000 == 0:
                break   #@todo: remove
                print str(i) + ' features of ' + str(len(features)) + ' done'


        classifiers = []
        used = []

        print 'Selecting classifiers..'
        sys.stdout.write('[' + ' '*20 + ']\r')
        sys.stdout.flush()
        for i in range(bag_count):

            classification_errors = dict()

            # normalize weights
            norm_factor = 1. / sum(map(lambda im: im.weight, images))
            for image in images:
                image.set_weight(image.weight * norm_factor)

            # select best weak classifier
            for feature, feature_votes in votes.iteritems():

                if feature in used:
                    continue

                # calculate error
                error = sum(map(lambda im, vote: im.weight if im.label != vote else 0, feature_votes[:,0], feature_votes[:,1]))
                # map error -> feature, use error as key to select feature with
                # smallest error later
                classification_errors[error] = feature

            # get best feature, i.e. with smallest error
            errors = classification_errors.keys()
            best_error = errors[np.argmin(errors)]
            feature = classification_errors[best_error]
            used.append(feature)
            feature_weight = 0.5 * np.log((1-best_error)/best_error)

            classifiers.append((feature, feature_weight))

            # update image weights
            best_feature_votes = votes[feature]
            for feature_vote in best_feature_votes:
                im = feature_vote[0]
                vote = feature_vote[1]
                if im.label != vote:
                    im.set_weight(im.weight * np.sqrt((1-best_error)/best_error))
                else:
                    im.set_weight(im.weight * np.sqrt(best_error/(1-best_error)))

            sys.stdout.write('[' + '='*(((i+1)*20)/bag_count) + ' '*(20-(((i+1)*20)/bag_count)) + ']\r')
            sys.stdout.flush()

        self.classifiers = classifiers

    def query(self, image):
        """
        if total vote is greather than zero than it's a face
        :param classifiers:
        :return:
        """
        total = 0
        for classifier in self.classifiers:
            total += classifier[0].get_vote(image) * classifier[1]

        if total > 0:
            return 1
        else:
            return -1