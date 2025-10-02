import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
    providedIn: 'root',
})
export class SnackBarService {
    constructor(private snackBar: MatSnackBar) {}

    show(message: string, action: string = 'Close', duration: number = 3000) {
        this.snackBar.open(message, action, { duration });
    }

    showError(
        message: string,
        action: string = 'Close',
        duration: number = 3000
    ) {
        this.snackBar.open(message, action, {
            duration,
            panelClass: 'snack-bar-error',
        });
    }
}
