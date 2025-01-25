import { Routes } from '@angular/router';
import { InitialFormComponent } from './initial-form/initial-form.component';
import { DynamicFormComponent } from './dynamic-form/dynamic-form.component';

export const routes: Routes = [
    {
        path: '',
        redirectTo: '/intial-form',
        pathMatch: 'full'
    },
    {
        path: 'intial-form',
        component: InitialFormComponent
    },
    {
        path: 'dynamic-form',
        component: DynamicFormComponent
    },
    {
        path: '**',
        redirectTo: '/intial-form'
    }
];
