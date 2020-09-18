import hail as hl
from gnomad.resources.resource_utils import (PedigreeResource, TableResource,
                                             VersionedPedigreeResource,
                                             VersionedTableResource)

from gnomad_qc.v3.resources.constants import (CURRENT_META_VERSION,
                                              CURRENT_PROJECT_META_VERSION,
                                              CURRENT_RELEASE, RELEASES)


# Samples metadata
def _meta_root_path(version: str = CURRENT_RELEASE) -> str:
    """
    Retrieves the path to the root metadata directory

    :param version: gnomAD release version
    :return: String representation of the path to the root metadata directory
    """
    return f"gs://gnomad/metadata/genomes_v{version}"


def meta_tsv_path(
    version: str = CURRENT_RELEASE, meta_version: str = CURRENT_META_VERSION
) -> str:
    """
    Gets the path to the finalized sample metadata information after sample QC

    :param version: gnomAD release version
    :param meta_version: metadata version to return
    :return: String path to the finalized metadata
    """
    return (
        f"{_meta_root_path(version)}/gnomad_v{version}_metadata_{meta_version}.tsv.gz"
    )


_meta_versions = {
    "2019-09-27": TableResource(
        path="gs://gnomad/metadata/genomes_v3/gnomad_v3_metadata_2019-09-27.ht"
    ),
    "2019-09-25": TableResource(
        path="gs://gnomad/metadata/genomes_v3/gnomad_v3_metadata_2019-09-25.ht"
    ),
}
_meta_versions["v3"] = _meta_versions["2019-09-27"]


_project_meta_versions = {
    "2020-09-11": TableResource(
        path="gs://gnomad/metadata/genomes_v3.1/2020-09-11_v3.1_project_meta.ht"
    ),
    "09-09-2019": TableResource(
        path="gs://gnomad/metadata/genomes_v3/09-09-2019_v3_project_meta.ht",
        import_func=hl.import_table,
        import_args={
            "paths": "gs://gnomad/metadata/genomes_v3/09-09-2019_v3_project_meta.txt",
            "impute": True,
            "key": "s",
            "min_partitions": 100,
        },
    ),
}
_project_meta_versions["v3"] = _project_meta_versions["09-09-2019"]
_project_meta_versions["v3.1"] = _project_meta_versions["2020-09-11"]


_pedigree_versions = {
    "final": PedigreeResource(
        "gs://gnomad/metadata/genomes_v3.1/gnomad_v3.1.fam", delimiter="\t",
    ),
    "v3.1_raw": PedigreeResource(
        "gs://gnomad/metadata/genomes_v3.1/gnomad_v3.1_raw.fam", delimiter="\t"
    ),
    "v3": PedigreeResource(
        "gs://gnomad/metadata/genomes_v3/gnomad_v3.fam", delimiter="\t",
    ),
    "v3_raw": PedigreeResource(
        "gs://gnomad/metadata/genomes_v3/gnomad_v3_raw.fam", delimiter="\t"
    ),
}


_trios_versions = {
    "final": PedigreeResource(
        "gs://gnomad/metadata/genomes_v3.1/gnomad_v3.1_trios.fam", delimiter="\t",
    ),
    "v3.1_raw": PedigreeResource(
        "gs://gnomad/metadata/genomes_v3.1/gnomad_v3.1_trios_raw.fam", delimiter="\t"
    ),
    "v3": PedigreeResource(
        "gs://gnomad/metadata/genomes_v3/gnomad_v3_trios.fam", delimiter="\t",
    ),
    "v3_raw": PedigreeResource(
        "gs://gnomad/metadata/genomes_v3/gnomad_v3_trios_raw.fam", delimiter="\t"
    ),
}


meta = VersionedTableResource(CURRENT_META_VERSION, _meta_versions)
project_meta = VersionedTableResource(
    CURRENT_PROJECT_META_VERSION, _project_meta_versions
)
pedigree = VersionedPedigreeResource("final", _pedigree_versions)
trios = VersionedPedigreeResource("final", _trios_versions)
ped_mendel_errors = VersionedTableResource(
    CURRENT_RELEASE,
    {
        release: TableResource(
            path=f"{_meta_root_path(release)}/gnomad_v{release}_ped_chr20_mendel_errors.ht"
        )
        for release in RELEASES
    },
)
