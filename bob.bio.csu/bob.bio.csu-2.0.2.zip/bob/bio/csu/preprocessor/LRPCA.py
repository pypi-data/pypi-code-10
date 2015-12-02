#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @date: Mon Oct 29 09:27:59 CET 2012
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import facerec2010
import pyvision
import numpy
import bob.bio.base

class LRPCA (bob.bio.base.preprocessor.Preprocessor):
  """This class defines a wrapper for the :py:class:`facerec2010.baseline.lda.LRPCA` class to be used as an image :py:class:`bob.bio.base.preprocessor.Preprocessor`.

  **Parameters:**

  TUNING : dict
    The tuning for the LRPCA algorithm as taken from the :py:attr:`facerec2010.baseline.lrpca.GBU_TUNING`.
  """

  def __init__(self, TUNING):
    bob.bio.base.preprocessor.Preprocessor.__init__(self, **TUNING)
    self.lrpca = facerec2010.baseline.lrpca.LRPCA(**TUNING)


  def __call__(self, image, annotations):
    """__call__(image, annotations) -> preprocessed
    Preprocesses the image using the :py:meth:`facerec2010.baseline.lrpca.LRPCA.preprocess` function.

    **Parameters:**

    image : :py:class:`pyvision.Image` or :py:class:`numpy.ndarray`
      The gray level or color image that should be preprocessed.

    annotations : dict
      The eye annotations for the image.
      They need to be specified as ``{'reye' : (re_y, re_x), 'leye' : (le_y, le_x)}``, where right and left is in subject perspective.

    **Returns:**

    preprocessed : numpy.ndarray
      The preprocessed image, in default Bob format.
    """
    assert isinstance(image, (pyvision.Image, numpy.ndarray))

    # assure that the eye positions are in the set of annotations
    if annotations is None or 'leye' not in annotations or 'reye' not in annotations:
      raise ValueError("The LRPCA image cropping needs eye positions, but they are not given.")

    # Warning! Left and right eye are mixed up here!
    # The lrpca preprocess expects left_eye_x < right_eye_x
    tile = self.lrpca.preprocess(
        image,
        rect=None,
        leye = pyvision.Point(annotations['reye'][1], annotations['reye'][0]),
        reye = pyvision.Point(annotations['leye'][1], annotations['leye'][0])
    )

    # pyvision used images in (x,y)-order.
    # To be consistent to the (y,x)-order in Bob, we have to transpose
    return tile.asMatrix2D().transpose()


  def read_original_data(self, image_file):
    """read_original_data(image_file) -> image

    Reads the original images using functionality from pyvision.

    **Parameters:**

    image_file : str
      The image file to be read, can contain a gray level or a color image.

    **Returns:**

    image : :py:class:`pyvision.Image`
      The image read from file.
    """
    # we use pyvision to read the images. Hence, we don't have to struggle with conversion here
    return pyvision.Image(str(image_file))
