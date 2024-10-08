/**
 * AIoD - RAIL
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.20240603-beta
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


export interface AIoDEntryRead {
  /**
   * Links to identifiers of persons responsible for maintaining the entry.
   */
  editor?: Array<number>;
  /**
   * Status of the entry (published, draft, rejected)
   */
  status?: string;
  /**
   * The datetime on which the metadata was last updated in the AIoD platform,in UTC.  Note the difference between `.aiod_entry.date_created` and `.date_published`: the former is automatically set to the datetime the resource was created on AIoD, while the latter can optionally be set to an earlier datetime that the resource was published on an external platform.
   */
  date_modified?: string;
  /**
   * The datetime on which the metadata was first published on the AIoD platform, in UTC.
   */
  date_created?: string;
}

