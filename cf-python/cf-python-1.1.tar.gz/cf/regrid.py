# -*- coding: utf-8 -*-
from numpy import array as numpy_array
from numpy import empty as numpy_empty
from numpy import where as numpy_where
from numpy import sum as numpy_sum
from .data.data import Data
from .functions import REGRID_LOGGING
from . import _found_ESMF
if _found_ESMF:
    import ESMF

class Regrid:
    """

Class containing all the methods required for accessing ESMF
regridding through ESMPY and the associated utility methods.

    """
    
    def __init__(self, srcfield, dstfield, srcfracfield, dstfracfield,
                 method='conservative'):
        """

Creates a handle for regridding fields from a source grid to a
destination grid that can then be used by the run_regridding method.

:Parameters:

    srcfield: ESMF.Field
        The source field with an associated grid to be used for
        regridding.

    dstfield: ESMF.Field
        The destination field with an associated grid to be used
        for regridding.

    srcfracfield: ESMF.Field
        A field to hold the fraction of the source field that
        contributes to conservative regridding.

    dstfracfield: ESMF.Field
        A field to hold the fraction of the source field that
        contributes to conservative regridding.

    method: string, optional
        By default the regridding method is conservative. If this
        parameter is set to 'bilinear' then multilinear interpolation
        is used.
    
        """
        # create a handle to the regridding method
        if method == 'conservative':
            regrid_method = ESMF.RegridMethod.CONSERVE
        elif method == 'bilinear':
            regrid_method = ESMF.RegridMethod.BILINEAR
        else:
            raise ValueError('Regrid method not recognised.')
        
        self.regridSrc2Dst = ESMF.Regrid(srcfield, dstfield, regrid_method=regrid_method,
                                         src_mask_values=numpy_array([0], dtype='int32'),
                                         dst_mask_values=numpy_array([0], dtype='int32'),
                                         src_frac_field=srcfracfield,
                                         dst_frac_field=dstfracfield,
                                         unmapped_action=ESMF.UnmappedAction.IGNORE)
    #--- End: def
    
    def destroy(self):
        """

Free the memory associated with the ESMF.Regrid instance.

        """
        self.regridSrc2Dst.destroy()
    #--- End: def
    
    @staticmethod
    def initialize():
        """

Check whether ESMF has been found. If not raise an import
error. Initialise the ESMPy manager. Whether logging is enabled or not
is determined by cf.REGRID_LOGGING. If it is then logging takes place
after every call to ESMPy.

:Returns:

    manager: ESMF.Manager
        A singleton instance of the ESMPy manager.

        """
        if not _found_ESMF:
            raise ImportError('The ESMF package is needed to support regridding.')
        
        manager = ESMF.Manager(debug=REGRID_LOGGING())
        return manager
    #--- End: def

    @staticmethod
    def create_grid(lon, lat, cyclic, mask=None):
        """

Create an ESMPy grid given 1D latitude and 1D longitude coordinates
for use as a source or destination grid in regridding. Optionally the
grid may have an associated mask.

:Parameters:

    lon : DimensionCoordinate
        The DimensionCoordinate containing the 1D longitude
        coordinates.

    lat : DimensionCoordinate
        The DimensionCoordinate containing the 1D latitude
        coordinates.

    cyclic : bool
        Whether or not the longitude is cyclic.

    mask : numpy.ndarray, optional
        An optional numpy array of booleans containing the grid points
        to mask.  Where the elements of mask are True the output grid
        is masked.

:Returns:

    out: ESMF.Grid
        The resulting ESMPy grid for use as a source or destination
        grid in regridding.

        """
        # Check the bounds for contiguity if they exist
        if lon.hasbounds and not lon.contiguous(overlap=False):
            raise ValueError('The longitude bounds must be contiguous.')
        #--- End: if
        if lat.hasbounds and not lon.contiguous(overlap=False):
            raise ValueError('The latitude bounds must be contiguous.')
        #--- End: if
        
        # Get the bounds, creating them if they do not exist
        x_bounds = lon.get_bounds(create=True).array
        y_bounds = lat.get_bounds(create=True).clip(-90, 90, 'degrees').array
        
        # Create empty grid
        max_index = numpy_array([lon.size, lat.size], dtype='int32')
        staggerLocs = [ESMF.StaggerLoc.CORNER, ESMF.StaggerLoc.CENTER]
        if cyclic:
            grid = ESMF.Grid(max_index, num_peri_dims=1, staggerloc=staggerLocs)
        else:
            grid = ESMF.Grid(max_index, staggerloc=staggerLocs)
        #--- End: if
        
        # Populate grid centres
        x, y = 0, 1
        gridXCentre = grid.get_coords(x, staggerloc=ESMF.StaggerLoc.CENTER)
        gridXCentre[...] = lon.array.reshape((lon.size, 1))
        gridYCentre = grid.get_coords(y, staggerloc=ESMF.StaggerLoc.CENTER)
        gridYCentre[...] = lat.array.reshape((1, lat.size))
        
        # Populate grid corners
        gridCorner = grid.coords[ESMF.StaggerLoc.CORNER]
        if cyclic:
            gridCorner[x][...] = x_bounds[:, 0].reshape(lon.size, 1)
        else:
            n = x_bounds.shape[0]
            tmp_x = numpy_empty(n + 1)
            tmp_x[:n] = x_bounds[:,0]
            tmp_x[n] = x_bounds[-1,1]
            gridCorner[x][...] = tmp_x.reshape(lon.size + 1, 1)
        #--- End: if
        n = y_bounds.shape[0]
        tmp_y = numpy_empty(n + 1)
        tmp_y[:n] = y_bounds[:,0]
        tmp_y[n] = y_bounds[-1,1]
        gridCorner[y][...] = tmp_y.reshape(1, lat.size + 1)
        
        # Add the mask if appropriate
        if not mask is None:
            gmask = grid.add_item(ESMF.GridItem.MASK)
            gmask[...] = 1
            gmask[mask] = 0
        #--- End: if
        
        return grid
    #--- End: def
    
    @staticmethod
    def create_2Dgrid(lon, lat, x_order, y_order, cyclic, mask=None):
        """

Create an ESMPy grid given 2D latitude and 2D longitude coordinates
for use as a source or destination grid in regridding. Optionally the
grid may have an associated mask.

:Parameters:

    lon: AuxiliaryCoordinate
        The AuxiliaryCoordinate containing the 2D longitude
        coordinates.

    lat : AuxiliaryCoordinate
        The AuxiliaryCoordinate containing the 2D latitude
        coordinates.

    x_order : tuple
        A tuple indicating the order of the x and y axes for
        longitude.

    y_order : tuple
        A tuple indicating the order of the x and y axes for
        latitude.

    cyclic : bool
        Whether or not the longitude is cyclic.

    mask : numpy.ndarray, optional
        An optional numpy array of booleans containing the grid
        points to mask.  Where the elements of mask are True the
        output grid is masked.

:Returns:

    out: ESMF.Grid
        The resulting ESMPy grid for use as a source or destination
        grid in regridding.

    out: bool
        A boolean indicating whether or not the grid has bounds.

        """
        # Get the shape of the grid
        shape = lon.transpose(x_order).shape
        if lat.shape != lon.shape:
            raise ValueError('The longitude and latitude coordinates must' +
                             ' have the same shape.')
        
        # Check whether bounds exist or not, and get them if they do
        hasbounds = lon.hasbounds and lat.hasbounds
        if hasbounds:
            x_bounds = lon.bounds
            y_bounds = lat.bounds.clip(-90, 90, 'degrees')
            if not x_bounds.contiguous(overlap=False):
                raise ValueError('The 2D longitude bounds must be contiguous.')
            if not y_bounds.contiguous(overlap=False):
                raise ValueError('The 2D latitude bounds must be contiguous.')
            
            n = x_bounds.shape[0]
            m = x_bounds.shape[1]
            x_bounds = x_bounds.array
            y_bounds = y_bounds.array
            
            tmp_x = numpy_empty((n + 1, m + 1))
            tmp_x[:n,:m] = x_bounds[:,:,0]
            tmp_x[:n,m] = x_bounds[:,-1,1]
            tmp_x[n,:m] = x_bounds[-1,:,3]
            tmp_x[n,m] = x_bounds[-1,-1,2]

            tmp_y = numpy_empty((n + 1, m + 1))
            tmp_y[:n,:m] = y_bounds[:,:,0]
            tmp_y[:n,m] = y_bounds[:,-1,1]
            tmp_y[n,:m] = y_bounds[-1,:,3]
            tmp_y[n,m] = y_bounds[-1,-1,2]

            x_bounds = tmp_x
            y_bounds = tmp_y
        
        # Create empty grid
        max_index = numpy_array(shape, dtype='int32')
        if hasbounds:
            staggerLocs = [ESMF.StaggerLoc.CORNER, ESMF.StaggerLoc.CENTER]
        else:
            staggerLocs = ESMF.StaggerLoc.CENTER
        if cyclic:
            grid = ESMF.Grid(max_index, num_peri_dims=1, staggerloc=staggerLocs)
        else:
            grid = ESMF.Grid(max_index, staggerloc=staggerLocs)
        
        # Populate grid centres
        x, y = 0, 1
        gridXCentre = grid.get_coords(x, staggerloc=ESMF.StaggerLoc.CENTER)
        gridXCentre[...] = lon.transpose(x_order).array
        gridYCentre = grid.get_coords(y, staggerloc=ESMF.StaggerLoc.CENTER)
        gridYCentre[...] = lat.transpose(y_order).array
        
        # Populate grid corners if there are bounds
        if hasbounds:
            gridCorner = grid.coords[ESMF.StaggerLoc.CORNER]
            x_bounds = x_bounds.transpose(x_order)
            y_bounds = y_bounds.transpose(y_order)
            if cyclic:
                x_bounds = x_bounds[:-1,:]
                y_bounds = y_bounds[:-1,:]
            gridCorner[x][...] = x_bounds
            gridCorner[y][...] = y_bounds
        
        # Add the mask if appropriate
        if not mask is None:
            gmask = grid.add_item(ESMF.GridItem.MASK)
            gmask[...] = 1
            gmask[mask] = 0
        #--- End: if
        
        return grid, hasbounds
    #--- End: def

#    @staticmethod
#    def create_cartesian_grid(coords, mask=None):
#        """
#
#Create a cartesian grid with between 1 and 3 dimensions given a tuple or list
#of dimension coordinates and optionally a mask. The number of coordinates
#passed will determine the dimensionality of the grid.
#
#:Parameters:
#
#    coords : tuple or list of cf.DimensionCoordinate objects
#        The coordinates specifying the grid. There must be between 1 and 3
#        elements.
#
#    mask : numpy.ndarray, optional
#        An optional numpy array of booleans containing the grid points to mask.
#        Where the elements of mask are True the output grid is masked.
#
#        """
#        
#        # Test the dimensionality of the list of coordinates
#        ndim = len(coords)
#        if ndim < 2 or ndim > 3:
#            raise ValueError('Cartesian grid must have 2 or 3 dimensions.')
#        #--- End: if
#        
#        shape = list()
#        for coord in coords:
#            shape.append(coord.size)
#        
#        # Initialize the grid
#        max_index = numpy_array(shape, dtype='int32')
#        staggerLocs = [ESMF.StaggerLoc.CORNER, ESMF.StaggerLoc.CENTER]
#        grid = ESMF.Grid(max_index, coord_sys=ESMF.CoordSys.CART,
#                         staggerloc=staggerLocs)
#        
#        # Populate the grid centres
#        for d in xrange(0, ndim):
#            gridDCentre = grid.get_coords(d, staggerloc=ESMF.StaggerLoc.CENTER)
#            gridDCentre[...] = coords[d].array.reshape([shape[d] if x == d else 1
#                                                       for x in xrange(0, ndim)])
#        #--- End: for
#        
#        # Populate grid corners
#        gridCorner = grid.coords[ESMF.StaggerLoc.CORNER]
#        for d in xrange(0, ndim):
#            if coords[d].hasbounds and not coords[d].contiguous(overlap=False):
#                raise ValueError('Coordinate ' + d + ' does not have contiguous bounds.')
#            #--- End: if
#            boundsD = coords[d].get_bounds(create=True).array
#            boundsD = numpy_append(boundsD[:, 0], boundsD[-1, 1])
#            gridCorner[d][...] = boundsD.reshape([shape[d] + 1 if x == d else 1
#                                                  for x in xrange(0, ndim)])
#        
#        # Add the mask if appropriate
#        if not mask is None:
#            gmask = grid.add_item(ESMF.GridItem.MASK)
#            gmask[...] = 1
#            gmask[mask] = 0
#        #--- End: if
#        
#        return grid
#    #--- End: def

    @staticmethod
    def create_field(grid, name):
        """

Create an ESMPy field for use as a source or destination field in
regridding given an ESMPy grid and a name.

:Parameters:

    grid : ESMF.Grid
        The ESMPy grid to use in creating the field.

    name : str
        The name to give the field.

:Returns:

    out : ESMF.Field
        The resulting ESMPy field for use as a source or destination
        field in regridding.

        """
        field = ESMF.Field(grid, name)
        return field
    #--- End: def
    
    def run_regridding(self, srcfield, dstfield):
        dstfield = self.regridSrc2Dst(srcfield, dstfield,
                                      zero_region=ESMF.Region.SELECT)
        return dstfield
    #--- End: def
    
    @staticmethod
    def concatenate_data(data_list, axis):
        """

Concatenates a list of Data objects into a single Data object along
the specified access (see cf.Data.concatenate for details). In the
case that the list contains only one element, that element is simply
returned.

:Parameters:

    data_list : list
        The list of data objects to concatenate.

    axis : int
        The axis along which to perform the concatenation.

:Returns:

    out : Data
        The resulting single Data object.

        """
        if len(data_list) > 1:
            return Data.concatenate(data_list, axis=axis)
        else:
            assert len(data_list) == 1
            return data_list[0]
        #--- End: if
    #--- End: def
    
    @staticmethod
    def reconstruct_sectioned_data(sections):
        """

Expects a dictionary of Data objects with ordering information as
keys, as output by the section method when called with a Data
object. Returns a reconstructed cf.Data object with the sections in
the original order.

:Parameters:

    sections : dict
        The dictionary or Data objects with ordering information as
        keys.

:Returns:

    out : Data
        The resulting reconstructed Data object.

        """
        ndims = len(sections.keys()[0])
        for i in range(ndims - 1, -1, -1):
            keys = sorted(sections.keys())
            if i==0:
                if keys[0][i] is None:
                    assert len(keys) == 1
                    return sections.values()[0]
                else:
                    data_list = []
                    for k in keys:
                        data_list.append(sections[k])
                    return Regrid.concatenate_data(data_list, i)
                #--- End: if
            else:
                if keys[0][i] is None:
                    pass
                else:
                    new_sections = {}
                    new_key = keys[0][:i]
                    data_list = []
                    for k in keys:
                        if k[:i] == new_key:
                            data_list.append(sections[k])
                        else:
                            new_sections[new_key] = Regrid.concatenate_data(data_list, i)
                            new_key = k[:i]
                            data_list = [sections[k]]
                        #--- End: if
                    new_sections[new_key] = Regrid.concatenate_data(data_list, i)
                    sections = new_sections
                #--- End: if
            #--- End: if
    #--- End: def
    
    @staticmethod
    def get_latlong(f, name):
        """
Retrieve the latitude and longitude coordinates of a field for
regridding and the associated informarion required. If 1D lat/long
coordinates are found then these are returned, otherwise 2D lat/long
coordinates are searched for and if found returned.

:Parameters:

    f : Field
        The field to retrieve coordinates from.

    name : string
        A name to identify the field in error messages.

:Returns:

    x : Coordinate
        The x coordinate (1D dimension coordinate or 2D
        auxilliary coordinate).

    y : Coordinate
        The y coordinate (1D dimension coordinate or 2D
        auxilliary coordinate).

    x_axis : string
        The key of the x dimension coordinate.

    y_axis : string
        The key of the y dimension coordinate.

    x_key : string
        The key of the x coordinate (1D dimension
        coordinate or 2D auxilliary coordinate).

    y_key : string
        The key of the y coordinate (1D dimension
        coordinate or 2D auxilliary coordinate).

    x_size : int
        The size of the x dimension coordinate.

    y_size : int
        The size of the y dimension coordinate.

    f_2D : bool
        True if 2D auxiliary coordinates are returned.

        """
        # Retrieve the field's X and Y dimension coordinates
        x = f.dims('X')
        y = f.dims('Y')
        if len(x) != 1 or len(y) != 1:
            raise ValueError('Unique dimension coordinates specifying the X' +
                             ' and Y axes of the ' + name + ' field not found.')
        #--- End: if
        x_axis, x = x.popitem()
        y_axis, y = y.popitem()
        x_key = x_axis
        y_key = y_axis        
        x_size = x.size
        y_size = y.size

        # If 1D latitude and longitude coordinates for the field are not found
        # search for 2D auxiliary coordinates.
        if not x.Units.islongitude or not y.Units.islatitude:
            lon_found = False
            lat_found = False
            for key, aux in f.auxs(ndim=2).iteritems():
                if aux.Units.islongitude:
                    if lon_found:
                        raise ValueError('The 2D auxiliary longitude coordinate' +
                                         ' of the ' + name + ' field is not unique.')
                    else:
                        lon_found = True
                        x = aux
                        x_key = key
                    #--- End: if
                #--- End: if
                if aux.Units.islatitude:
                    if lat_found:
                        raise ValueError('The 2D auxiliary latitude coordinate' +
                                         ' of the ' + name + ' field is not unique.')
                    else:
                        lat_found = True
                        y = aux
                        y_key = key
                    #--- End: if
                #--- End: if
            if not lon_found or not lat_found:
                raise ValueError('Both longitude and latitude coordinates' +
                                 ' were not found for the ' + name + ' field.')
            f_2D = True
        else:
            f_2D = False
        #--- End: if
        
        return x, y, x_axis, y_axis, x_key, y_key, x_size, y_size, f_2D
    #--- End: def
    
    @staticmethod
    def compute_mass_grid(valuefield, areafield, dofrac=False, fracfield=None, 
                      uninitval=422397696.):
        '''

Compute the mass of a data field.

:Parameters:

    
    valuefield : ESMF.Field
        This contains data values of a field built on the cells
        of a grid.

    areafield : ESMF.Field
        This contains the areas associated with the grid cells.

    fracfield : ESMF.Field
        This contains the fractions of each cell which contributed
        to a regridding operation involving 'valuefield.

    dofrac : bool
        This gives the option to not use the 'fracfield'.

    uninitval : float
        The value uninitialised cells take.

:Returns:

    mass : float
        The mass of the data field is computed.

        '''
        mass = 0.0
        areafield.get_area()
        
        ind = numpy_where(valuefield.data != uninitval)
        
        if dofrac:
            mass = numpy_sum(areafield.data[ind] * valuefield.data[ind] * fracfield.data[ind])
        else:
            mass = numpy_sum(areafield.data[ind] * valuefield.data[ind])
        
        return mass
    #--- End: def

#--- End: class
