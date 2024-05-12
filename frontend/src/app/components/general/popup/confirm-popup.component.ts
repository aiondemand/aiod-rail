import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ConfirmPopupInput } from 'src/app/models/popup-input';

@Component({
  selector: 'confirm-app-popup',
  templateUrl: './confirm-popup.component.html',
  styleUrls: ['./confirm-popup.component.scss']
})
export class ConfirmPopupComponent {

  constructor(
    @Inject(MAT_DIALOG_DATA) public popupInput: ConfirmPopupInput
  ) { }

  ngOnInit(): void {
    console.log(this.popupInput);
  }
}
