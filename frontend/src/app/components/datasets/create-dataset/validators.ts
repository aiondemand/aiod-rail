import { FormControl } from "@angular/forms";
import { Platform } from "src/app/models/platform";

export function isPlatformSupported(platform: Platform | string): boolean {
    const platformName = typeof platform == 'string' ? platform : platform.name;
    return ['huggingface', 'aiod'].includes(platformName);
}

export function nameValidator(control: FormControl) {
    const nameValue = control.value;
    const platformValue = control.parent?.get('platform')?.value;
    if (platformValue == 'huggingface') {
        // check if nameValue is compliant with huggingface dataset name
        // it can only contain alphanumerics, _, - and .
        if (!/^[a-zA-Z0-9_\.-]+$/.test(nameValue)) {
            return { nameValidation: true };
        }
    }
    return null;
}

export function platformIsSupportedValidator(control: FormControl) {
    const platformValue = control?.value;
    return isPlatformSupported(platformValue) ? null : { platformIsSupportedValidation: true };
}

export function keywordsValidator(control: FormControl) {
    // only check keywords for huggingface
    if (control.parent?.get('platform')?.value != 'huggingface') {
        return null;
    }

    const keywordsValue = control.value;
    if (keywordsValue) {
        for (let keyword of keywordsValue.split(',')) {
            // check if the keyword starts with alphanumeric
            if (!/^[a-zA-Z]+.*$/.test(keyword.trim())) {
                return { keywordsValidation: true };
            }
        }
    }
    return null;
}