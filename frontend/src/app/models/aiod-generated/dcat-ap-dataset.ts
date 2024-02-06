/**
 * AIoD Metadata Catalogue
 * This is the Swagger documentation of the AIoD Metadata Catalogue. For the Changelog, refer to <a href=\"https://github.com/aiondemand/AIOD-rest-api/releases\">https://github.com/aiondemand/AIOD-rest-api/releases</a>.
 *
 * The version of the OpenAPI document: 1.2.20231219
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { DcatAPIdentifier } from './dcat-ap-identifier';
import { XSDDateTime } from './xsd-date-time';


/**
 * Base class for all DCAT-AP objects
 */
export interface DcatAPDataset {
  [key: string]: any | any;


    id: any | null;
    type?: any | null;
    /**
     * This property contains a free-text account of the Dataset
     */
    dctdescription?: any | null;
    /**
     * This property contains a name given to the Dataset
     */
    dcttitle: any | null;
    /**
     * This property contains contact information that can be used for sending comments about the Dataset.
     */
    dcatcontactPoint?: any | null;
    dcatdistribution?: any | null;
    dcatkeyword?: any | null;
    dctpublisher?: DcatAPIdentifier;
    dcatcreator?: any | null;
    foafpage?: any | null;
    /**
     * This property refers to a web page that provides access to the Dataset, its Distributions and/or additional information. It is intended to point to a landing page at the original data provider, not to a page on a site of a third party, such as an aggregator.
     */
    dcatlandingPage?: any | null;
    dctissued?: XSDDateTime;
    dctmodified?: XSDDateTime;
    owlversionInfo?: any | null;
}
