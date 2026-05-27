from arcgis.features import FeatureSet, FeatureLayer
from arcgis.gis import GIS
from typing import Literal, Optional
import warnings
import os
from tqdm import tqdm

def get_agol_feature_layer(
    feature_layer_url: str = None,
    filter_expression: str = "1=1",
    fields: str = "*",
    return_geometry: bool = False,
    attachments_action: Literal['metadata', 'download'] = 'metadata',
    attachments_dir: Optional[str] = None,
    gis: GIS = None
):
    """
    Get a feature layer from ArcGIS Online and return a dictionary with the features and attachments metadata.

    Parameters:
    feature_layer_url (str): The URL of the feature layer.
    filter_expression (str): The filter expression to use when querying the feature layer.
    fields (str): The fields to return when querying the feature layer.
    return_geometry (bool): Whether to return the geometry of the features.
    attachments_action (Literal['metadata', 'download']): The action to take when downloading attachments.
    attachments_dir (Optional[str]): The directory to download attachments to.
    gis (GIS): The GIS object to use for the query.

    Returns:
    Tuple[List[Dict], List[Dict]]: A tuple containing a list of features and a list of attachments metadata.
    """
    feature_layer_missing = feature_layer_url is None
    filter_expression_invalid = (not isinstance(filter_expression, str))
    fields_invalid = (not isinstance(fields, str))
    return_geometry_invalid = (not isinstance(return_geometry, bool))
    attachments_action_invalid = (attachments_action not in ['metadata', 'download'])
    missing_attachments_dir = (attachments_action == 'download' and attachments_dir is None)

    if feature_layer_missing:
        raise Exception("You must provide a feature layer url.")

    if filter_expression_invalid:
        raise Exception("The filter expression must be a string.")
    
    if fields_invalid:
        raise Exception("The fields must be a string.")

    if return_geometry_invalid:
        raise Exception("The return_geometry must be a boolean.")

    if attachments_action_invalid:
        raise Exception("The attachments_action must be either 'metadata' or 'download'.")
    
    if missing_attachments_dir:
        raise Exception("You must provide an attachments_dir if you want to download attachments.")

    try:
        agol_feature_layer = FeatureLayer(feature_layer_url, gis=gis)
    except Exception as e:
        raise Exception(f"Error while loading feature layer << {feature_layer_url} >>: {e}")

    if not agol_feature_layer.properties.hasAttachments and attachments_action == 'download':
        attachments_action = 'metadata'
        warnings.warn("The feature layer does not have attachments. Only metadata will be returned.")

    agol_features = agol_feature_layer.query(
        where = filter_expression,
        out_fields = fields,
        return_geometry = return_geometry
    )

    object_ids = agol_feature_layer.query(
        where = filter_expression,
        return_ids_only = True
    ).get('objectIds')
    
    agol_features_dict = agol_features.to_dict()

    out_dict = [out_dict['attributes'] for out_dict in agol_features_dict['features']]

    if attachments_action == 'metadata':
        return out_dict

    attachments_dir = attachments_dir or 'arcgis_attachments'
    os.makedirs(attachments_dir, exist_ok=True)

    # Chatgpt here
    oid_field = agol_feature_layer.properties.objectIdField
    oid_to_feature = {feat[oid_field]: feat for feat in out_dict}
    #end of chatgpt

    result = list()

    for oid in tqdm(
        object_ids,
        desc="Downloading attachments",
        unit="feature",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [Time elapsed: {elapsed} < ETA: {remaining}, {rate_fmt}]"
    ):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            attachments_info = agol_feature_layer.attachments.get_list(oid=oid)

        if not attachments_info:
            tqdm.write(f"[WARNING] Feature OID={oid} has no attachments. Skipping.")
            continue

        feature_context = oid_to_feature.get(oid, {})

        for att in attachments_info:
            agol_feature_layer.attachments.download(
                oid=oid,
                attachment_id=att['id'],
                save_path=attachments_dir
            )
            result.append({
                **feature_context,
                "attachment_id": att['id'],
                "attachment_name": att['name'],
                "attachment_size": att.get('size'),
                "attachment_content_type": att.get('contentType'),
            })

    return result
