# Machine Learning - An Introduction
- Presenter : Dr. Anoop Namboodiri

## The pattern recognition process
- Training Data
- Feature extraction
- Feature space representation : The biggest problem in ML is a good
feature representation, given a good feature space representation, KNN is
more than good enough to classify them.
- Classifier Design
- Classifier Model -> Classifier -> Class label

## How do we distinguish between classes ?
- find the equation of a separating boundary in the feature space
- Find a model for each class in the feature space (the probability
distribution for each class). For example : A dog/cat classifier can model
both classes as probability distributions. 

## K-NN

### Boundaries between every pair of samples
- Voronoi Tessalation
- Error rate (with increasing number of training samples) is at-most twice
that of the ideal classifier.
- bayesian classifier are always the ideal classifier

### Distance metrics
- assumption : vectors are always column vectors
- Iso surfaces : It is a surface with all points at the same distance from
a point/set of points. Iso-surface for 2d euclidean distance are concentric
surface
- L0 and L_infinity norm
- Mahalanobis distance
- Hamming distance : How many dimensions the vector is different. Mainly
used for binary vectors
- Cosine distance
- Jaccard distance - does not follow traingle inequality
- edit distance - doesn't follow traingle inequality
