import { Platform } from '../models/platform';

export function formatPlatformName(platform: string | Platform): string {
    const platformName = typeof platform == 'string' ? platform : platform.name;
    switch (platformName.trim().toLowerCase()) {
        case 'openml':
            return 'OpenML';
        case 'huggingface':
            return 'HuggingFace';
        case 'aiod':
            return 'AIoD';
        case 'example':
        case 'zenodo':
        default:
            return platformName.charAt(0).toUpperCase() + platformName.slice(1);
    }
}
