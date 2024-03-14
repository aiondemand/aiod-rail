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


/**
 * Metadata of the metadata: when was the metadata last updated, with what identifiers is it known on other platforms, etc.
 */
export interface AIoDEntryCreate { 
    /**
     * Links to identifiers of persons responsible for maintaining the entry.
     */
    editor?: Array<number>;
    /**
     * Status of the entry (published, draft, rejected)
     */
    status?: string;
}

