import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ConfirmPopupInput, ConfirmPopupResponse } from 'src/app/models/popup';

@Component({
  selector: 'confirm-app-popup',
  templateUrl: './confirm-popup.component.html',
  styleUrls: ['./confirm-popup.component.scss']
})
export class ConfirmPopupComponent {

  constructor(
    @Inject(MAT_DIALOG_DATA) public popupInput: ConfirmPopupInput,
    private dialogRef: MatDialogRef<ConfirmPopupComponent>,
  ) { }

  ngOnInit(): void {}

  yes() {
    this.dialogRef.close(ConfirmPopupResponse.Yes);
  }

  no() {
    this.dialogRef.close(ConfirmPopupResponse.No);
  }

  thirdOption() {
    this.dialogRef.close(ConfirmPopupResponse.ThirdOption);
  }

}
