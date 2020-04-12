pro netcdfToTiff
  
  file = file_search('D:\try\', '*.nc', count=count)
  s = sort(file)
  print, file[s]
  aaaaaaa
  
  for i=0, count-1 do begin
    nid = ncdf_open(file[i])
    
    ;read rh
    rhid = ncdf_varid(nid, 'r')
    ncdf_varget, nid, rhid, rh
    ncdf_attget, nid, rhid, 'scale_factor', scale_factor
    ncdf_attget, nid, rhid, 'add_offset', add_offset
    rh = rh * scale_factor + add_offset
    
    print, scale_factor, add_offset

    ps = [0.25, 0.25]
    mc = [0, 0, 73, 54]
    map_info = envi_map_info_create(/geographic, mc=mc, ps=ps, datum='WGS-84')
    
    filename = strsplit(file[i], '\', /extract)
    filename = strsplit(filename[-1], '.', /extract)
    envi_write_envi_file, rh, out_name = 'D:\try\' + filename[0] + '.tif', map_info = map_info, /no_open
    
    print, filename[0]
    
  endfor
end