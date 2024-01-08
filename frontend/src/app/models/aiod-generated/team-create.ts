/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { AIoDEntryCreate } from './aio-d-entry-create';
import { Text } from './text';


/**
 * The AIoDConcept is the top-level (abstract) class in AIoD.
 */
export interface TeamCreate { 
    /**
     * The external platform from which this resource originates. Leave empty if this item originates from AIoD. If platform is not None, the platform_resource_identifier should be set as well.
     */
    platform?: any | null;
    /**
     * A unique identifier issued by the external platform that\'s specified in \'platform\'. Leave empty if this item is not part of an external platform.
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
     * A ballpark figure of the per hour cost to hire this team.
     */
    price_per_hour_euro?: any | null;
    /**
     * The number of persons that are part of this team.
     */
    size?: any | null;
    aiod_entry?: AIoDEntryCreate;
    /**
     * An alias for the item, commonly used for the resource instead of the name.
     */
    alternate_name?: any | null;
    /**
     * The objective of this AI resource.
     */
    application_area?: any | null;
    /**
     * Contact information of persons/organisations that can be contacted about this resource.
     */
    contact?: any | null;
    /**
     * Contact information of persons/organisations that created this resource.
     */
    creator?: any | null;
    description?: Text;
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
    /**
     * Images or videos depicting the resource or associated with it. 
     */
    media?: any | null;
    /**
     * The persons that are a member of this team. The leader should also be added as contact.
     */
    member?: any | null;
    /**
     * Notes on this AI resource.
     */
    note?: any | null;
    /**
     * The organisation of which this team is a part.
     */
    organisation?: any | null;
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
}

