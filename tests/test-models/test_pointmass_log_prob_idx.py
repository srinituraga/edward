from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import edward as ed
import numpy as np
import tensorflow as tf

from edward.models import PointMass
from scipy import stats


def pointmass_logpmf_vec(x, params):
  """Vectorized log-density for point mass distribution."""
  return np.equal(x, params).astype(np.float32)


def _test(shape, n):
  rv = PointMass(shape, params=tf.zeros(shape) + 0.5)
  rv_sample = rv.sample(n)
  x = rv_sample.eval()
  x_tf = tf.constant(x, dtype=tf.float32)
  params = rv.params.eval()
  for idx in range(shape[0]):
    assert np.allclose(rv.log_prob_idx((idx, ), x_tf).eval(),
                       pointmass_logpmf_vec(x[:, idx], params[idx]))


class test_pointmass_log_prob_idx_class(tf.test.TestCase):

  def test_1d(self):
    ed.set_seed(98765)
    with self.test_session():
      _test((1, ), 1)
      _test((1, ), 5)
      _test((5, ), 1)
      _test((5, ), 5)
