import openmc
# Point OpenMC to the cross_sections.xml file with all cross section data.
openmc.config["cross_sections"] = "/opt/nuclear_data/endfb-vii.1-hdf5/cross_sections.xml"
################################################################################
# Describe the materials of the problem.
################################################################################
uranium = openmc.Material()
uranium.add_element("U", 1.0, enrichment=20.0)
materials = openmc.Materials([uranium])
materials.export_to_xml()
################################################################################
# Describe the geometry of the problem.
################################################################################
sphere_surface = openmc.Sphere(r=1.025)
sphere_surface.boundary_type = "vacuum"

cell = openmc.Cell()
cell.region = -sphere_surface
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
settings.run_mode = "eigenvalue"
settings.export_to_xml()

openmc.run()
