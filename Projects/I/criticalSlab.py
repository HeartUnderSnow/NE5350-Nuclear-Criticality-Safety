import openmc
# Point OpenMC to the cross_sections.xml file with all cross section data.
openmc.config["cross_sections"] = "/opt/nuclear_data/endfb-vii.1-hdf5/cross_sections.xml"
################################################################################
# Describe the materials of the problem.
################################################################################

uranium = openmc.Material()
uranium.add_element("U", 1.0, enrichment=5.90)
materials = openmc.Materials([uranium])
materials.export_to_xml()
################################################################################
# Describe the geometry of the problem.
################################################################################

width = 6.5

# Begin by defining a surface at the left and right.
left = openmc.XPlane(0.0)
left.boundary_type = "vacuum"
right = openmc.XPlane(width)
right.boundary_type = "vacuum"

# Combine surfaces together into a cell
cell = openmc.Cell()
cell.region = +left & -right
cell.fill = uranium

geom = openmc.Geometry([cell])
geom.export_to_xml()

################################################################################
# Configure the settings.
################################################################################

settings = openmc.Settings()
settings.particles = 100_000
settings.batches = 100 + 50
settings.inactive = 50
# Create an initial uniform spatial source distribution over the domain.
bounds = [0.0, 0.0, 0.0, width, 0.0, 0.0]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:])
settings.source = openmc.IndependentSource(space=uniform_dist)
settings.run_mode = "eigenvalue"
settings.export_to_xml()
# Run in parallel with four threads.
openmc.run(threads=4)

