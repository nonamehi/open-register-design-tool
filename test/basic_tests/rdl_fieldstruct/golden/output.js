/*   Ordt 190725.01 autogenerated file 
 *   Input: ./rdl_fieldstruct/test.rdl
 *   Parms: ./rdl_fieldstruct/test.parms
 *   Date: Sun Nov 17 17:00:57 EST 2019
 */

register_set foo "Registers for foo" {

  address = 0x0;
  register_width = 32;
  register areg "areg register" {
    address = 0x0;
    repeat = 2;
    nop[3];
    integer fs3_fld2[1] "fs3_fld2 field" param {
      access_mode = READ_WRITE;
      reset = unknown;
    };
    integer fs3_fld1[4] "fs3_fld1 field" param {
      access_mode = READ_WRITE;
      reset = 0x0;
    };
    nop[9];
    integer hier_fs_fs2_fld2[1] "hier_fs_fs2_fld2 field" param {
      access_mode = READ_WRITE;
      reset = unknown;
    };
    nop[4];
    integer hier_fs_fs2_fld1[4] "hier_fs_fs2_fld1 field" param {
      access_mode = READ_WRITE;
      reset = 0x0;
    };
    integer hier_fs_fld1[1] "hier_fs_fld1 field" param {
      access_mode = READ_WRITE;
      reset = unknown;
    };
    integer hier_fs_fs1_fld2[1] "hier_fs_fs1_fld2 field" param {
      access_mode = READ_WRITE;
      reset = unknown;
    };
    integer hier_fs_fs1_fld1[4] "hier_fs_fs1_fld1 field" param {
      access_mode = READ_WRITE;
      reset = 0x0;
    };
  };
  
  register blabla "blabla register" {
    address = 0x8;
    nop[4];
    integer fs3_1_fld2[1] "fs3_1_fld2 field" param {
      access_mode = READ_WRITE;
      reset = unknown;
    };
    integer fs3_1_fld1[4] "fs3_1_fld1 field" param {
      access_mode = READ_WRITE;
      reset = 0x0;
    };
    nop[3];
    integer fs3_0_fld2[1] "fs3_0_fld2 field" param {
      access_mode = READ_WRITE;
      reset = unknown;
    };
    integer fs3_0_fld1[4] "fs3_0_fld1 field" param {
      access_mode = READ_WRITE;
      reset = 0x0;
    };
    integer fs1_2_fld2[1] "fs1_2_fld2 field" param {
      access_mode = READ_WRITE;
      reset = unknown;
    };
    integer fs1_2_fld1[4] "fs1_2_fld1 field" param {
      access_mode = READ_WRITE;
      reset = 0x0;
    };
    integer fs1_1_fld2[1] "fs1_1_fld2 field" param {
      access_mode = READ_WRITE;
      reset = unknown;
    };
    integer fs1_1_fld1[4] "fs1_1_fld1 field" param {
      access_mode = READ_WRITE;
      reset = 0x0;
    };
    integer fs1_0_fld2[1] "fs1_0_fld2 field" param {
      access_mode = READ_WRITE;
      reset = unknown;
    };
    integer fs1_0_fld1[4] "fs1_0_fld1 field" param {
      access_mode = READ_WRITE;
      reset = 0x0;
    };
  };
  
  register_set_size = 0xc;
};

