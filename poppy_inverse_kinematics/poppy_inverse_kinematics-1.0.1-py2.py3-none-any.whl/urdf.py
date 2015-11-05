import xml.etree.ElementTree as ET


base_link_name = "base_link"

current_link = base_link


def find_next_joint(current_link):
    # Trouver le joint attaché
    has_next = False
    next_joint = 0

    for joint in root.iter("joint"):
        if joint.find("parent").attrib["link"] == current_link.attrib["name"]:
            has_next = True
            next_joint = joint
    return(has_next, next_joint)


def find_next_link(current_joint):
    # Trouver le next_link
    has_next = False
    next_link = 0
    for link in root.iter("link"):
        if link.attrib["name"] == current_joint.find("child").attrib["link"]:
            next_link = link
            has_next = True
    return(has_next, next_link)


def get_urdf_parameters(urdf_file, base_link_name):
    tree = ET.parse(urdf_file)
    root = tree.getroot()

    # Récupération du 1er link
    for link in root.iter('link'):
        if link.attrib["name"] == base_link_name:
            base_link = link

    has_next = True
    current_link = base_link
    node_type = "link"
    joints = []
    links = []
    while(has_next):
        if node_type == "link":
            links.append(link)
            (has_next, current_joint) = find_next_joint(current_link)
            node_type = "joint"
        elif node_type == "joint":
            joints.append(current_joint)
            (has_next, current_link) = find_next_link(current_joint)

            node_type = "link"

    parameters = []
    for joint in joints:
        parameters.append((joint.find("origin").attrib["xyz"], joint.find("axis").attrib["xyz"]))

    return(parameters)

print(get_urdf_parameters('ergo.urdf', base_link_name))
