import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {MatButtonModule} from '@angular/material/button';
import {MatDividerModule} from '@angular/material/divider';
import {MatIconModule} from '@angular/material/icon';
import {FormBuilder, Validators, FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatStepperModule} from '@angular/material/stepper';
import {MatOptionModule} from '@angular/material/core';
import {MatSelectModule} from '@angular/material/select';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  imports: [
    RouterOutlet, 
    MatButtonModule, 
    MatDividerModule, 
    MatIconModule, 
    MatStepperModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule, 
    MatOptionModule, 
    MatSelectModule
  ]
})
export class AppComponent {

  title = 'frontend';
  models = ["CTGAN", "TVAE"];

  // Training form

  modelFormGroup = this._formBuilderTraining.group({
    modelsCtrl: [this.models[0], Validators.required, ],
  });

  dataFormGroup = this._formBuilderTraining.group({
    dataCtrl: ['', Validators.required, ],
  });

  // Generation form

  samplesFormGroup = this._formBuilderGeneration.group({
    samplesCtrl: ['1', Validators.required, ],
  });

  constructor(private _formBuilderGeneration: FormBuilder, private _formBuilderTraining: FormBuilder) {}

  onGenerateClick(){
    const n_samples_str = this.samplesFormGroup.value.samplesCtrl

    if (n_samples_str != null && n_samples_str != undefined){
      const n_samples = parseInt(n_samples_str)
      console.log(n_samples)
    }
  }

  onTrainClick(){
    const model = this.modelFormGroup.value.modelsCtrl
  }

  onEvaluateClick(){}
}
