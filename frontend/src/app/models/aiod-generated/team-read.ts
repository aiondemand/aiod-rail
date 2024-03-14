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


export interface TeamRead { 
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
     * A ballpark figure of the per hour cost to hire this team.
     */
    price_per_hour_euro?: number;
    /**
     * The number of persons that are part of this team.
     */
    size?: number;
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
    /**
     * Contact information of persons/organisations that created this resource.
     */
    creator?: Array<number>;
    description?: Text;
    has_part?: Array<number>;
    /**
     * A business domain where a resource is or can be used.
     */
    industrial_sector?: Array<string>;
    is_part_of?: Array<number>;
    /**
     * Keywords or tags used to describe this resource, providing additional context.
     */
    keyword?: Array<string>;
    /**
     * Images or videos depicting the resource or associated with it. 
     */
    media?: Array<Distribution>;
    /**
     * The persons that are a member of this team. The leader should also be added as contact.
     */
    member?: Array<number>;
    /**
     * Notes on this AI resource.
     */
    note?: Array<Note>;
    /**
     * The organisation of which this team is a part.
     */
    organisation?: number;
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
    identifier: number;
}

