#   Ordt 190725.01 autogenerated file 
#   Input: ./rdl_hier_01/test.rdl
#   Parms: ./rdl_hier_01/test.parms
#   Date: Sun Nov 17 17:09:27 EST 2019
#


from enum import Enum, auto

class ordt_drv_error(Enum):
    BAD_TAG = auto()
    BAD_PATH = auto()
    BAD_ADDRESS = auto()

class ordt_drv_return_type(Enum):
    REG = auto()
    REGSET = auto()
    FIELD = auto()

class ordt_drv_path_element:
    
    def __init__(self, name_str):
            sub_lst = name_str.split('[')
            if len(sub_lst)==2:
                self.name = sub_lst[0]
                self.idx = sub_lst[1].rstrip(']')
            else:
                self.name = name_str
                self.idx = 1
    

class ordt_drv_field:
    
    def __init__(self, name, loidx, width, readable, writeable, reset):
        self.name = name
        self.loidx = loidx
        self.width = width
        self.readable = readable
        self.writeable = writeable
        self.reset = reset
    

class ordt_drv_element:
    ORDT_PIO_DRV_VERBOSE = True
    
    def __init__(self, name):
        self.name = name
    
    def get_address_using_version(self, version, pathstr, address_in):
        path = self.get_pathlist(pathstr)
        if path:
            return self.get_address_using_list(version, path, False, address_in)
        if __class__.ORDT_PIO_DRV_VERBOSE:
            print('--> invalid path: ' + pathstr)
        return {'error':ordt_drv_error.BAD_PATH}
    
    def get_path_instance_list_using_version(self, version, pathstr, path_instance_list_in):
        path = self.get_pathlist(pathstr)
        if path:
            return self.get_path_instance_list_using_list(version, path, False, path_instance_list_in)
        if __class__.ORDT_PIO_DRV_VERBOSE:
            print('--> invalid path: ' + pathstr)
        return {'error':ordt_drv_error.BAD_PATH}
    
    def get_version(self, tag):
        if tag == 'base_map':
            return 0
        else:
            return -1
    
    def get_tags(self):
        tags = []
        tags.append('base_map')
        return tags
    
    def get_address_using_tag(self, tag, pathstr, address_in):
        version = self.get_version(tag)
        if version<0:
            if __class__.ORDT_PIO_DRV_VERBOSE:
                print('--> invalid tag: ' + tag)
            return {'error':ordt_drv_error.BAD_TAG}
        return self.get_address_using_version(version, pathstr, address_in)
    
    def get_path_instance_list_using_tag(self, tag, pathstr, path_instance_list_in):
        version = self.get_version(tag)
        if version<0:
            if __class__.ORDT_PIO_DRV_VERBOSE:
                print('--> invalid tag: ' + tag)
            return {'error':ordt_drv_error.BAD_TAG}
        return self.get_path_instance_list_using_version(version, pathstr, path_instance_list_in)
    
    def get_pathlist(self, pathstr):
        pathlist = []
        lst = pathstr.split('.')
        for str_elem in lst:
            path_elem = ordt_drv_path_element(str_elem)
            pathlist.append(path_elem)
        return pathlist
    
    def get_path_using_tag(self, tag, address, path_in):
        version = self.get_version(tag)
        if version<0:
            if __class__.ORDT_PIO_DRV_VERBOSE:
                print('--> invalid tag: ' + tag)
            return {'error':ordt_drv_error.BAD_TAG}
        return self.get_path_using_version(version, address, path_in)
    

class ordt_drv_regset_child:
    
    def __init__(self, version_map, child, reps, offset, stride):
        self.version_map = version_map
        self.child = child
        self.reps = reps
        self.offset = offset
        self.stride = stride
    
    def find_offset(self, address_in):
        if not self.stride:
            return (0, self.child.name)
        if (address_in < self.offset) or (address_in >= self.offset + self.reps*self.stride):
            return (0, None)
        if self.reps < 2:
            return (self.offset, '.' + self.child.name)
        index = (address_in - self.offset) // self.stride
        return (self.offset + index*self.stride, '.' + self.child.name + '[' + str(index) + ']')
    

class ordt_drv_regset(ordt_drv_element):
    
    def __init__(self, name):
        super().__init__(name)
        self.children = []
    
    def get_address_using_list(self, version, path, bypass_names, address_in):
        if not path:
            return {'error':ordt_drv_error.BAD_PATH}
        pelem = path[0]
        if not bypass_names:
            path.pop(0)
            if not path:
                return {'type':ordt_drv_return_type.REGSET, 'address':address_in, 'children':self.get_child_names(version)}
            pelem = path[0]
        for child in self.children:
            if ((1<<version) & child.version_map) and (bypass_names or (pelem.name == child.child.name)):
                address = address_in + child.offset
                if child.reps > 1:
                    address += child.stride*int(pelem.idx)
                return child.child.get_address_using_list(version, path, False, address)
        if __class__.ORDT_PIO_DRV_VERBOSE:
            print('--> unable to find child ' + pelem.name + ' in regset ' + self.name)
        return {'error':ordt_drv_error.BAD_PATH}
    
    def get_path_instance_list_using_list(self, version, path, bypass_names, path_instance_list_in):
        if not path:
            return {'error':ordt_drv_error.BAD_PATH}
        pelem = path[0]
        if not bypass_names:
            path.pop(0)
            if not path:
                return {'type':ordt_drv_return_type.REGSET, 'instances':path_instance_list_in}
            pelem = path[0]
        for child in self.children:
            if ((1<<version) & child.version_map) and (bypass_names or (pelem.name == child.child.name)):
                path_instance_list = path_instance_list_in.copy()
                path_instance_list.append(child)
                return child.child.get_path_instance_list_using_list(version, path, False, path_instance_list)
        if __class__.ORDT_PIO_DRV_VERBOSE:
            print('--> unable to find child ' + pelem.name + ' in regset ' + self.name)
        return {'error':ordt_drv_error.BAD_PATH}
    
    def add_child(self, version_map, child, reps, offset, stride):
        new_child = ordt_drv_regset_child(version_map, child, reps, offset, stride)
        self.children.append(new_child)
    
    def get_child_names(self, version):
        childnames = []
        for child in self.children:
            if (1<<version) & child.version_map:
                childnames.append(child.child.name)
        return childnames
    
    def get_path_using_version(self, version, address_in, path_in):
        for child in self.children:
            if (1<<version) & child.version_map:
                (match_addr, match_path) = child.find_offset(address_in)
                if match_path:
                    return child.child.get_path_using_version(version, address_in - match_addr, path_in + match_path)
        return {'error':ordt_drv_error.BAD_ADDRESS}
    

class ordt_drv_reg(ordt_drv_element):
    
    def __init__(self, name, width):
        super().__init__(name)
        self.fields = []
        self.width = width
    
    def get_address_using_list(self, version, path, bypass_names, address_in):
        if not path:
            return {'error':ordt_drv_error.BAD_PATH}
        path.pop(0)
        if not path:
            return {'type':ordt_drv_return_type.REG, 'address':address_in, 'width':self.width, 'fields':self.fields}
        if __class__.ORDT_PIO_DRV_VERBOSE:
            pelem = path[0]
            print('--> invalid child ' + pelem.name + ' specified in reg ' + self.name)
        return {'error':ordt_drv_error.BAD_PATH}
    
    def get_path_instance_list_using_list(self, version, path, bypass_names, path_instance_list_in):
        if not path:
            return {'error':ordt_drv_error.BAD_PATH}
        path.pop(0)
        if not path:
            return {'type':ordt_drv_return_type.REG, 'instances':path_instance_list_in}
        if len(path) == 1:
            fname = path[0].name
            fld = self.get_field_by_name(fname)
            if fld:
                path_instance_list = path_instance_list_in.copy()
                path_instance_list.append(fld)
                return {'type':ordt_drv_return_type.FIELD, 'instances':path_instance_list}
        if __class__.ORDT_PIO_DRV_VERBOSE:
            pelem = path[0]
            print('--> invalid child ' + pelem.name + ' specified in reg ' + self.name)
        return {'error':ordt_drv_error.BAD_PATH}
    
    def get_field_by_name(self, name):
        for fld in self.fields:
            if fld.name == name:
                return fld
    
    def add_field(self, name, loidx, width, readable, writeable, reset):
        new_field = ordt_drv_field(name, loidx, width, readable, writeable, reset)
        self.fields.append(new_field)
    
    def get_path_using_version(self, version, address_in, path_in):
        return {'type':ordt_drv_return_type.REG, 'path':path_in}
    

class ordt_drv_root(ordt_drv_regset):
    base_address = 0
    
    def __init__(self):
        super().__init__('root')
        self.build()
    
    def build(self):
        no_opt_reg_72 = ordt_drv_reg('no_opt_reg', 32)
        no_opt_reg_72.add_field('lsb_field', 0, 16, True, False, 65535)
        opt_reg_73 = ordt_drv_reg('opt_reg', 32)
        opt_reg_73.add_field('lsb_field', 0, 16, True, False, 65535)
        config_regs_39 = ordt_drv_reg('config_regs', 32)
        config_regs_39.add_field('lsb_field', 0, 16, True, True, 65535)
        config_regs_39.add_field('msb_field', 16, 16, True, True, 0)
        state_regs_40 = ordt_drv_reg('state_regs', 32)
        state_regs_40.add_field('lsb_field', 0, 16, True, False, 65535)
        ext_base_regs_41 = ordt_drv_regset('ext_base_regs')
        ext_base_regs_41.add_child(1, config_regs_39, 8, 0, 4)
        ext_base_regs_41.add_child(1, state_regs_40, 8, 256, 4)
        base_regs_38 = ordt_drv_regset('base_regs')
        base_regs_38.add_child(1, config_regs_39, 8, 0, 4)
        base_regs_38.add_child(1, state_regs_40, 8, 256, 4)
        l3_child_51 = ordt_drv_regset('l3_child')
        l3_child_51.add_child(1, base_regs_38, 1, 0, 512)
        l3_child_51.add_child(1, ext_base_regs_41, 1, 2048, 512)
        l2_r16_child_44 = ordt_drv_regset('l2_r16_child')
        l2_r16_child_44.add_child(1, ext_base_regs_41, 1, 4096, 512)
        l2_r16_child_44.add_child(1, base_regs_38, 1, 0, 512)
        l2_r16_child_44.add_child(1, l3_child_51, 1, 8192, 4096)
        l2_s8_child_58 = ordt_drv_regset('l2_s8_child')
        l2_s8_child_58.add_child(1, ext_base_regs_41, 1, 4096, 512)
        l2_s8_child_58.add_child(1, base_regs_38, 1, 0, 512)
        l2_s8_child_58.add_child(1, l3_child_51, 1, 8192, 4096)
        base_map_37 = ordt_drv_regset('base_map')
        base_map_37.add_child(1, no_opt_reg_72, 1, 262144, 4)
        base_map_37.add_child(1, opt_reg_73, 1, 262160, 4)
        base_map_37.add_child(1, l2_r16_child_44, 1, 131072, 16384)
        base_map_37.add_child(1, l2_s8_child_58, 1, 196608, 16384)
        base_map_37.add_child(1, base_regs_38, 1, 0, 512)
        base_map_37.add_child(1, ext_base_regs_41, 1, 65536, 512)
        self.add_child(1, base_map_37, 1, 0, 0)
    
    def get_address_using_version(self, version, pathstr, address_in):
        path = self.get_pathlist(pathstr)
        if path:
            return self.get_address_using_list(version, path, True, address_in)
        if __class__.ORDT_PIO_DRV_VERBOSE:
            print('--> invalid path: ' + pathstr)
        return {'error':ordt_drv_error.BAD_PATH}
    
    def get_path_instance_list_using_version(self, version, pathstr, path_instance_list_in):
        path = self.get_pathlist(pathstr)
        if path:
            return self.get_path_instance_list_using_list(version, path, True, path_instance_list_in)
        if __class__.ORDT_PIO_DRV_VERBOSE:
            print('--> invalid path: ' + pathstr)
        return {'error':ordt_drv_error.BAD_PATH}
    
    def get_address(self, tag, pathstr):
        '''return address given a path string and tag'''
        return self.get_address_using_tag(tag, pathstr, __class__.base_address)
    
    def get_path_instance_list(self, tag, pathstr):
        '''return list of model elements given a path string and tag'''
        return self.get_path_instance_list_using_tag(tag, pathstr, [])
    
    def get_path(self, tag, address):
        '''return path string given an address and tag'''
        return self.get_path_using_tag(tag, address, '')
    

