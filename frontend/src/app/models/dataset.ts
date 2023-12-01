import * as backend from './backend-generated/dataset';

export interface Dataset extends backend.Dataset {
    is_in_my_saved: boolean;
}

export interface DatasetFormValue {
    name: string,
    description: string,
    platform: string,
    version: string,
    alternateNames: string,
    keywords: string,
    huggingface: { username: string }
}

export function createDatasetFromFormData(
    formValue: DatasetFormValue
) {
    let platformIdentifier = getPlatformIdentifier(formValue);

    let dataset: Dataset = {
        platform: formValue.platform,
        platform_resource_identifier: platformIdentifier,
        name: platformIdentifier,
        same_as: getSameAs(formValue, platformIdentifier),
        description: { plain: formValue.description },
        alternate_name: getAlternateNames(formValue),
        keyword: getKeywords(formValue),
        is_in_my_saved: false,
        citation: [],
        distribution: [],
        is_part_of: [],
        has_part: [],
        is_accessible_for_free: true,
        creator: [],
        identifier: 0,
        version: formValue.version,
    }

    return dataset;
}

function getPlatformIdentifier(formValue: DatasetFormValue): string {
    switch (formValue.platform) {
        case 'openml':
            return '0';
        case 'huggingface':
        //   return `${formValue.huggingface.username}/${formValue.name}`
          return formValue.huggingface.username + `${formValue.huggingface.username ? '/' : ''}` + `${formValue.name}`;
        case 'aiod':
            return formValue.name;
        default:
            throw new Error('Unknown platform: ' + formValue.platform);
    }
}

function getSameAs(formValue: DatasetFormValue, platformIdentifier: string): string {
    switch (formValue.platform) {
        case 'openml':
            return 'https://www.openml.org/api/v1/json/data/3';
        case 'huggingface':
            // return `https://huggingface.co/datasets/${formValue.huggingface.username}`
            // + `${formValue.huggingface.username ? '/' : ''}` + `${formValue.name}`;
            return `https://huggingface.co/datasets/${platformIdentifier}`;
        case 'aiod':
        default:
            return formValue.name;
    }
}

function getAlternateNames(formValue: DatasetFormValue): string[] {
    if (formValue.alternateNames?.trim().length == 0) {
        return [];
    }

    return formValue.alternateNames
        .split(',')
        .map((alternateName: string) => alternateName.trim());
}

function getKeywords(formValue: DatasetFormValue): string[] {
    if (formValue.keywords?.trim().length == 0) {
        return [];
    }

    return formValue.keywords
        .split(',')
        .map((keyword: string) => keyword.trim());
}
