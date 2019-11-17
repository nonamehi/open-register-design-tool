//   Ordt 190725.01 autogenerated file 
//   Input: ./rdl_uvmmem_lite/test.rdl
//   Parms: ./rdl_uvmmem_lite/test.parms
//   Date: Sun Nov 17 17:09:38 EST 2019
//

#include "ordt_pio_common.hpp"
#include "ordt_pio_drv.hpp"

// ------------------ ordt_drv_path_element methods ------------------

ordt_drv_path_element::ordt_drv_path_element(std::string _m_name, int _m_idx)
  : m_name(_m_name),
    m_idx(_m_idx) {
}

// ------------------ ordt_drv_field methods ------------------

ordt_drv_field::ordt_drv_field(std::string _m_name, int _m_loidx, int _m_width, bool _m_readable, bool _m_writeable)
  : m_name(_m_name),
    m_loidx(_m_loidx),
    m_width(_m_width),
    m_readable(_m_readable),
    m_writeable(_m_writeable) {
}

// ------------------ ordt_drv_element methods ------------------

std::list<std::string>  ordt_drv_element::split(const std::string &text, char sep, bool trim_rb) {
  std::list<std::string> tokens;
  std::size_t start = 0, end = 0, end_adj = 0;
  while ((end = text.find(sep, start)) != std::string::npos) {
    if (trim_rb && ((end_adj = text.find(']', start)) != std::string::npos) && (end_adj<end))
      tokens.push_back(text.substr(start, end_adj - start));
    else
      tokens.push_back(text.substr(start, end - start));
    start = end + 1;
  }
  if (trim_rb && ((end_adj = text.find(']', start)) != std::string::npos))
    tokens.push_back(text.substr(start, end_adj - start));
  else
    tokens.push_back(text.substr(start));
  return tokens;
}

int  ordt_drv_element::get_version(const std::string tag) {
  if (tag == "top") return 0;
  else return -1;
}

std::list<ordt_drv_path_element>  ordt_drv_element::get_path(const std::string pathstr) {
  std::list<ordt_drv_path_element> pathlist;
  std::list<std::string> lst = split(pathstr, '.', true);
  for(auto const& str_elem: lst) {
     std::list<std::string> sub_lst = split(str_elem, '[', false);
     if (sub_lst.size()==2) {
       pathlist.emplace_back(sub_lst.front(), std::stoi(sub_lst.back()));
     }
     else {
       pathlist.emplace_back(sub_lst.front(), 1);
     }
  }
  return pathlist;
}

ordt_drv_element::ordt_drv_element(std::string _m_name)
  : m_name(_m_name) {
}

int  ordt_drv_element::get_address_using_version(const int version, const std::string pathstr, uint64_t &address, std::list<ordt_drv_field> &fields) {
  std::list<ordt_drv_path_element> path = get_path(pathstr);
  if (path.size()>0) return get_address_using_list(version, path, false, address, fields);
  #ifdef ORDT_PIO_DRV_VERBOSE
     std::cout << "--> invalid path: " << pathstr << "\n";
  #endif
  return 4;
}

std::vector<std::string>  ordt_drv_element::get_tags() {
  std::vector<std::string> tags;
  tags.push_back("top");
  return tags;
}

int  ordt_drv_element::get_address(const std::string tag, const std::string pathstr, uint64_t &address, std::list<ordt_drv_field> &fields) {
  int version = get_version(tag);
  if (version<0) {
  #ifdef ORDT_PIO_DRV_VERBOSE
     std::cout << "--> invalid tag: " << tag << "\n";
  #endif
    return 2;
  }
  return get_address_using_version(version, pathstr, address, fields);
}

// ------------------ ordt_drv_regset_child methods ------------------

ordt_drv_regset_child::ordt_drv_regset_child(int _m_map, std::shared_ptr<ordt_drv_element> _m_child, int _m_reps, uint64_t _m_offset, uint64_t _m_stride)
  : m_map(_m_map),
    m_child(_m_child),
    m_reps(_m_reps),
    m_offset(_m_offset),
    m_stride(_m_stride) {
}

// ------------------ ordt_drv_regset methods ------------------

ordt_drv_regset::ordt_drv_regset(std::string _m_name)
  : ordt_drv_element(_m_name),
    m_children() {
}

int  ordt_drv_regset::get_address_using_list(const int version, std::list<ordt_drv_path_element> &path, const bool bypass_names, uint64_t &address, std::list<ordt_drv_field> &fields) {
  if (path.empty())
    return 8;
  ordt_drv_path_element pelem = path.front();
  if (!bypass_names) {
    path.pop_front();
    if (path.empty())
      return 0;
    pelem = path.front();
  }
  for (auto const &child: m_children) {
    if (((1<<version) & child.m_map) && (bypass_names || (pelem.m_name == child.m_child->m_name))) {
      address += child.m_offset;
      if (child.m_reps>1) address += (child.m_stride*pelem.m_idx);
      return child.m_child->get_address_using_list(version, path, false, address, fields);
    }
  }
  #ifdef ORDT_PIO_DRV_VERBOSE
  std::cout << "--> unable to find child " << pelem.m_name << " in regset " << m_name << "\n";
  #endif
  return 8;
}

void  ordt_drv_regset::add_child(int _m_map, std::shared_ptr<ordt_drv_element> _m_child, int _m_reps, uint64_t _m_offset, uint64_t _m_stride) {
  ordt_drv_regset_child new_child(_m_map, _m_child, _m_reps, _m_offset, _m_stride);
  m_children.push_back(new_child);
}

// ------------------ ordt_drv_reg methods ------------------

ordt_drv_reg::ordt_drv_reg(std::string _m_name)
  : ordt_drv_element(_m_name),
    m_fields() {
}

int  ordt_drv_reg::get_address_using_list(const int version, std::list<ordt_drv_path_element> &path, const bool bypass_names, uint64_t &address, std::list<ordt_drv_field> &fields) {
  if (path.empty())
    return 8;
  path.pop_front();
  if (path.empty()) {
    fields = m_fields;
    return 0;
  }
  #ifdef ORDT_PIO_DRV_VERBOSE
  ordt_drv_path_element pelem = path.front();
  std::cout << "--> invalid child " << pelem.m_name << " specified in reg " << m_name << "\n";
  #endif
  return 8;
}

void  ordt_drv_reg::add_field(std::string _m_name, int _m_loidx, int _width, bool _m_readable, bool _m_writeable) {
  ordt_drv_field new_field(_m_name, _m_loidx, _width, _m_readable, _m_writeable);
  m_fields.push_back(new_field);
}

// ------------------ ordt_drv_root methods ------------------

ordt_drv_root::ordt_drv_root()
  : ordt_drv_regset("root") {
  build();
}

void  ordt_drv_root::build() {
  std::shared_ptr<ordt_drv_reg> sr_repeat1_3 = std::make_shared<ordt_drv_reg>("sr_repeat1");
  sr_repeat1_3->add_field("fld1", 0, 32, true, true);
  std::shared_ptr<ordt_drv_reg> srmem1_6 = std::make_shared<ordt_drv_reg>("srmem1");
  srmem1_6->add_field("fld1", 0, 32, true, true);
  std::shared_ptr<ordt_drv_reg> wrmem1_7 = std::make_shared<ordt_drv_reg>("wrmem1");
  wrmem1_7->add_field("fld1", 0, 16, true, true);
  wrmem1_7->add_field("fld2", 16, 16, true, true);
  wrmem1_7->add_field("fld3", 32, 16, true, true);
  wrmem1_7->add_field("fld4", 48, 16, true, true);
  wrmem1_7->add_field("fld5", 64, 16, true, true);
  wrmem1_7->add_field("fld6", 80, 16, true, true);
  wrmem1_7->add_field("fld7", 96, 16, true, true);
  wrmem1_7->add_field("fld8", 112, 16, true, true);
  std::shared_ptr<ordt_drv_reg> sr_repeat3_5 = std::make_shared<ordt_drv_reg>("sr_repeat3");
  sr_repeat3_5->add_field("fld1", 0, 32, true, true);
  std::shared_ptr<ordt_drv_reg> sr_repeat2_4 = std::make_shared<ordt_drv_reg>("sr_repeat2");
  sr_repeat2_4->add_field("fld1", 0, 32, true, true);
  std::shared_ptr<ordt_drv_reg> wr1_2 = std::make_shared<ordt_drv_reg>("wr1");
  wr1_2->add_field("fld1", 0, 16, true, true);
  wr1_2->add_field("fld2", 16, 16, true, true);
  wr1_2->add_field("fld3", 32, 16, true, true);
  wr1_2->add_field("fld4", 48, 16, true, true);
  wr1_2->add_field("fld5", 64, 16, true, true);
  wr1_2->add_field("fld6", 80, 16, true, true);
  wr1_2->add_field("fld7", 96, 16, true, true);
  wr1_2->add_field("fld8", 112, 16, true, true);
  std::shared_ptr<ordt_drv_reg> sr1_1 = std::make_shared<ordt_drv_reg>("sr1");
  sr1_1->add_field("fld1", 0, 32, true, true);
  std::shared_ptr<ordt_drv_regset> top_0 = std::make_shared<ordt_drv_regset>("top");
  top_0->add_child(1, sr_repeat1_3, 1, 512, 4);
  top_0->add_child(1, srmem1_6, 100, 8192, 4);
  top_0->add_child(1, wrmem1_7, 300, 131072, 16);
  top_0->add_child(1, sr_repeat3_5, 1, 520, 4);
  top_0->add_child(1, sr_repeat2_4, 1, 516, 4);
  top_0->add_child(1, wr1_2, 1, 256, 16);
  top_0->add_child(1, sr1_1, 1, 0, 4);
  add_child(1, top_0, 1, 0, 0);
}

int  ordt_drv_root::get_address_using_version(const int version, const std::string pathstr, uint64_t &address, std::list<ordt_drv_field> &fields) {
  address=0;
  fields.clear();
  std::list<ordt_drv_path_element> path = get_path(pathstr);
  if (path.size()>0) return get_address_using_list(version, path, true, address, fields);
  #ifdef ORDT_PIO_DRV_VERBOSE
     std::cout << "--> invalid path: " << pathstr << "\n";
  #endif
  return 4;
}

