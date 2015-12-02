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

class LDAIR (bob.bio.base.preprocessor.Preprocessor):
  """This class defines a wrapper for the :py:class:`facerec2010.baseline.lda.LRLDA` class to be used as an image :py:class:`bob.bio.base.preprocessor.Preprocessor`.

  **Parameters:**

  REGION_ARGS
    The region arguments as taken from :py:attr:`facerec2010.baseline.lda.CohortLDA_REGIONS`.

  REGION_KEYWORDS
    The region keywords as taken from :py:attr:`facerec2010.baseline.lda.CohortLDA_KEYWORDS`.
  """

  def __init__(self, REGION_ARGS, REGION_KEYWORDS):
    bob.bio.base.preprocessor.Preprocessor.__init__(self, **REGION_KEYWORDS)
    self.ldair = facerec2010.baseline.lda.LRLDA(REGION_ARGS, **REGION_KEYWORDS)
    self.layers = len(REGION_ARGS)


  def __call__(self, image, annotations):
    """Preprocesses the image using the LDA-IR preprocessor :py:meth:`facerec2010.baseline.lda.LRLDA.preprocess`.

    **Parameters:**

    image : :py:class:`pyvision.Image` or :py:class:`numpy.ndarray`
      The color image that should be preprocessed.

    annotations : dict
      The eye annotations for the image.
      They need to be specified as ``{'reye' : (re_y, re_x), 'leye' : (le_y, le_x)}``, where right and left is in subject perspective.

    **Returns:**

    preprocessed : 3D numpy.ndarray
      The preprocessed color image, in default Bob format.
    """

    # assure that the eye positions are in the set of annotations
    if annotations is None or 'leye' not in annotations or 'reye' not in annotations:
      raise ValueError("The LDA-IR image cropping needs eye positions, but they are not given.")

    if isinstance(image, numpy.ndarray):
      if len(image.shape) != 3:
        raise ValueError("The LDA-IR image cropping needs color images.")
      image = pyvision.Image(numpy.transpose(image, (0, 2, 1)).astype(numpy.float64))

    assert isinstance(image, pyvision.Image)

    # Warning! Left and right eye are mixed up here!
    # The ldair preprocess expects left_eye_x < right_eye_x
    tiles = self.ldair.preprocess(
        image,
        leye = pyvision.Point(annotations['reye'][1], annotations['reye'][0]),
        reye = pyvision.Point(annotations['leye'][1], annotations['leye'][0])
    )

    # LDAIR preprocessing spits out 4D structure, i.e., [Matrix]
    # with each element of the outer list being identical
    # so we just have to copy the first image

    assert len(tiles) == self.layers
    assert (tiles[0].asMatrix3D() == tiles[1].asMatrix3D()).all()

    # Additionally, pyvision used images in (x,y)-order.
    # To be consistent to the (y,x)-order in the facereclib, we have to transpose
    color_image = tiles[0].asMatrix3D()
    out_images = numpy.ndarray((color_image.shape[0], color_image.shape[2], color_image.shape[1]), dtype = numpy.uint8)

    # iterate over color layers
    for j in range(color_image.shape[0]):
      out_images[j,:,:] = color_image[j].transpose()[:,:]

    # WARNING! This contradicts the default way, images are written. Here, we write full color information!
    return out_images


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
