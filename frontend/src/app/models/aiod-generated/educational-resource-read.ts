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
import { Distribution } from './distribution';
import { Note } from './note';
import { Text } from './text';
import { AIoDEntryRead } from './aio-d-entry-read';
import { Location } from './location';


export interface EducationalResourceRead { 
    /**
     * The external platform from which this resource originates. Leave empty if this item originates from AIoD. If platform is not None, the platform_resource_identifier should be set as well.
     */
    platform?: string;
    /**
     * A unique identifier issued by the external platform that\'s specified in \'platform\'. Leave empty if this item is not part of an external platform. For example, for HuggingFace, this should be the <namespace>/<dataset_name>, and for Openml, the OpenML identifier.
     */
    platform_resource_identifier?: string;
    name: string;
    /**
     * The datetime (utc) on which this resource was first published on an external platform. Note the difference between `.aiod_entry.date_created` and `.date_published`: the former is automatically set to the datetime the resource was created on AIoD, while the latter can optionally be set to an earlier datetime that the resource was published on an external platform.
     */
    date_published?: string;
    /**
     * Url of a reference Web page that unambiguously indicates this resource\'s identity.
     */
    same_as?: string;
    /**
     * An approximate or recommendation of the time required to use or complete the educational resource.
     */
    time_required?: string;
    /**
     * The primary mode of accessing this educational resource.
     */
    access_mode?: Array<string>;
    /**
     * This resource can be identified by its own identifier, but also by the resource_identifier.
     */
    ai_resource_identifier?: number;
    aiod_entry?: AIoDEntryRead;
    /**
     * An alias for the item, commonly used for the resource instead of the name.
     */
    alternate_name?: Array<string>;
    /**
     * The objective of this AI resource.
     */
    application_area?: Array<string>;
    /**
     * Contact information of persons/organisations that can be contacted about this resource.
     */
    contact?: Array<number>;
    content?: Text;
    /**
     * Contact information of persons/organisations that created this resource.
     */
    creator?: Array<number>;
    description?: Text;
    /**
     * The level or levels of education for which this resource is intended.
     */
    educational_level?: Array<string>;
    has_part?: Array<number>;
    /**
     * The language(s) of the educational resource, in ISO639-3.
     */
    in_language?: Array<string>;
    /**
     * A business domain where a resource is or can be used.
     */
    industrial_sector?: Array<string>;
    is_part_of?: Array<number>;
    /**
     * Keywords or tags used to describe this resource, providing additional context.
     */
    keyword?: Array<string>;
    location?: Array<Location>;
    /**
     * Images or videos depicting the resource or associated with it. 
     */
    media?: Array<Distribution>;
    /**
     * Notes on this AI resource.
     */
    note?: Array<Note>;
    /**
     * The high-level study schedule available for this educational resource. \"self-paced\" is mostly used for MOOCS, Tutorials and short courses without interactive elements; \"scheduled\" is used for scheduled courses with interactive elements that is not a full-time engagement; \"full-time\" is used for programmes or intensive courses that require a full-time engagement from the student.
     */
    pace?: string;
    /**
     * Minimum or recommended requirements to make use of this educational resource.
     */
    prerequisite?: Array<string>;
    /**
     * URLs of relevant resources. These resources should not be part of AIoD (use relevant_resource otherwise). This field should only be used if there is no more specific field.
     */
    relevant_link?: Array<string>;
    relevant_resource?: Array<number>;
    relevant_to?: Array<number>;
    /**
     * The research area is similar to the scientific_domain, but more high-level.
     */
    research_area?: Array<string>;
    /**
     * The scientific domain is related to the methods with which an objective is reached.
     */
    scientific_domain?: Array<string>;
    /**
     * The intended users of this educational resource.
     */
    target_audience?: Array<string>;
    /**
     * The type of educational resource.
     */
    type?: string;
    identifier: number;
}

