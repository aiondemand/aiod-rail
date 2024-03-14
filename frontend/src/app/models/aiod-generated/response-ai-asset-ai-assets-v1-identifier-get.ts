/**
 * AIoD Metadata Catalogue
 * This is the Swagger documentation of the AIoD Metadata Catalogue. For the Changelog, refer to <a href=\"https://github.com/aiondemand/AIOD-rest-api/releases\">https://github.com/aiondemand/AIOD-rest-api/releases</a>.
 *
 * The version of the OpenAPI document: 1.3.20240308
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { MLModelRead } from './ml-model-read';
import { PublicationRead } from './publication-read';
import { ComputationalAssetRead } from './computational-asset-read';
import { CaseStudyRead } from './case-study-read';
import { DatasetRead } from './dataset-read';
import { Text } from './text';
import { ExperimentRead } from './experiment-read';
import { AIoDEntryRead } from './aio-d-entry-read';
import { DatasetSize } from './dataset-size';
import { Location } from './location';


export interface ResponseAiAssetAiAssetsV1IdentifierGet { 
    /**
     * The external platform from which this resource originates. Leave empty if this item originates from AIoD. If platform is not None, the platform_resource_identifier should be set as well.
     */
    platform?: any | null;
    /**
     * A unique identifier issued by the external platform that\'s specified in \'platform\'. Leave empty if this item is not part of an external platform. For example, for HuggingFace, this should be the <namespace>/<dataset_name>, and for Openml, the OpenML identifier.
     */
    platform_resource_identifier?: any | null;
    name: any | null;
    /**
     * The datetime (utc) on which this resource was first published on an external platform. Note the difference between `.aiod_entry.date_created` and `.date_published`: the former is automatically set to the datetime the resource was created on AIoD, while the latter can optionally be set to an earlier datetime that the resource was published on an external platform.
     */
    date_published?: any | null;
    /**
     * Url of a reference Web page that unambiguously indicates this resource\'s identity.
     */
    same_as?: any | null;
    /**
     * A flag to signal that this asset is accessible at no cost.
     */
    is_accessible_for_free?: any | null;
    /**
     * The version of this asset.
     */
    version?: any | null;
    /**
     * The International Standard Serial Number, ISSN, an identifier for serial publications.
     */
    issn?: any | null;
    /**
     * The technique, technology, or methodology used in a dataset, corresponding to the method used for measuring the corresponding variable(s).
     */
    measurement_technique?: any | null;
    /**
     * The temporalCoverage of a CreativeWork indicates the period that the content applies to, i.e. that it describes, a textual string indicating a time period in ISO 8601 time interval format. In the case of a Dataset it will typically indicate the relevant time period in a precise notation (e.g. for a 2011 census dataset, the year 2011 would be written \'2011/2012\').
     */
    temporal_coverage?: any | null;
    ai_asset_identifier?: any | null;
    /**
     * This resource can be identified by its own identifier, but also by the resource_identifier.
     */
    ai_resource_identifier?: any | null;
    aiod_entry?: AIoDEntryRead;
    /**
     * An alias for the item, commonly used for the resource instead of the name.
     */
    alternate_name?: any | null;
    /**
     * The objective of this AI resource.
     */
    application_area?: any | null;
    /**
     * A bibliographic reference.
     */
    citation?: any | null;
    /**
     * Contact information of persons/organisations that can be contacted about this resource.
     */
    contact?: any | null;
    /**
     * Contact information of persons/organisations that created this resource.
     */
    creator?: any | null;
    description?: Text;
    distribution?: any | null;
    /**
     * Links to identifiers of the agents (person or organization) that supports this dataset through some kind of financial contribution. 
     */
    funder?: any | null;
    has_part?: any | null;
    /**
     * A business domain where a resource is or can be used.
     */
    industrial_sector?: any | null;
    is_part_of?: any | null;
    /**
     * Keywords or tags used to describe this resource, providing additional context.
     */
    keyword?: any | null;
    license?: any | null;
    /**
     * Images or videos depicting the resource or associated with it. 
     */
    media?: any | null;
    /**
     * Notes on this AI resource.
     */
    note?: any | null;
    /**
     * URLs of relevant resources. These resources should not be part of AIoD (use relevant_resource otherwise). This field should only be used if there is no more specific field.
     */
    relevant_link?: any | null;
    relevant_resource?: any | null;
    relevant_to?: any | null;
    /**
     * The research area is similar to the scientific_domain, but more high-level.
     */
    research_area?: any | null;
    /**
     * The scientific domain is related to the methods with which an objective is reached.
     */
    scientific_domain?: any | null;
    /**
     * The size of this dataset, for example the number of rows. The file size should not be included here, but in distribution.content_size_kb.
     */
    size?: DatasetSize;
    /**
     * A location that describes the spatial aspect of this dataset. For example, a point where all the measurements were collected.
     */
    spatial_coverage?: Location;
    identifier: any | null;
    /**
     * A Permanent Identifier (e.g. DOI) for the entity
     */
    permanent_identifier?: any | null;
    /**
     * The International Standard Book Number, ISBN, used to identify published books or, more rarely, journal issues.
     */
    isbn?: any | null;
    content?: Text;
    /**
     * The identifier of an AI asset for which the Knowledge Asset acts as an information source
     */
    documents?: any | null;
    /**
     * The type of machine learning model.
     */
    type?: any | null;
    /**
     * A webpage that shows the current status of this asset.
     */
    status_info?: any | null;
    /**
     * A permanent identifier for the model, for example a digital object identifier (DOI). Ideally a url.
     */
    pid?: any | null;
    /**
     * A human readable description of the overall workflow of the experiment.
     */
    experimental_workflow?: any | null;
    /**
     * A human-readable description of the settings under which the experiment was executed.
     */
    execution_settings?: any | null;
    /**
     * A description of how the output of the experiment matches the experiments in the paper.
     */
    reproducibility_explanation?: any | null;
    /**
     * Labels awarded on the basis of the reproducibility of this experiment.
     */
    badge?: any | null;
    /**
     * Related experiments.
     */
    related_experiment?: any | null;
}

