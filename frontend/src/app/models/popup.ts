export interface ConfirmPopupInput {
    message: string;
    acceptBtnMessage?: string;
    declineBtnMessage?: string;
    thirdOptionBtnMessage?: string;
}

export enum ConfirmPopupResponse {
    Yes = "Yes",
    No = "No",
    ThirdOption = "ThirdOption"
}