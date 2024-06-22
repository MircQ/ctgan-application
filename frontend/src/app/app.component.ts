import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {MatButtonModule} from '@angular/material/button';
import {MatDividerModule} from '@angular/material/divider';
import {MatIconModule} from '@angular/material/icon';
import {FormBuilder, Validators, FormsModule, ReactiveFormsModule, FormControl} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatStepperModule} from '@angular/material/stepper';
import {MatOptionModule} from '@angular/material/core';
import {MatSelectModule} from '@angular/material/select';
import { BackendService } from './services/backend.service';
import {saveAs} from "file-saver";

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
    MatSelectModule,
  ],
})
export class AppComponent {

  title = 'CTGAN/TVAE application';
  models = ["CTGAN", "TVAE"];


  // Training form

  trainingData: File | null = null;
  trainingFileName: string | null = null;

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

  // Evaluation form

  syntheticData: File 
  syntheticDataFileName: string | null = null;

  realData: File
  realDataFileName: ?string

  constructor(
    private _formBuilderGeneration: FormBuilder, 
    private _formBuilderTraining: FormBuilder,
    private _backendService: BackendService
  ) {}

  onTrainingDataFileSelected(event: any) {

    const file:File = event.target.files[0];

    if (file) {

        this.trainingFileName = file.name;

        this.trainingData = file;
    }
  }

  onSyntheticDataFileSelected(event: any) {

    const file:File = event.target.files[0];

    if (file) {

        this.syntheticDataFileName = file.name;

        this.syntheticData = file;
    }
  }

  onRealDataFileSelected(event: any) {

    const file:File = event.target.files[0];

    if (file) {

        this.realDataFileName = file.name;

        this.realData = file;
    }
  }

  onTrainClick(){

    const model = this.modelFormGroup.value.modelsCtrl;

    if (model != undefined && model != null && this.trainingData != null ){
      this._backendService.train(model, this.trainingData).subscribe((res) => {
        console.log("OK")
      })
    }
  }

  onGenerateClick(){
    const n_samples_str = this.samplesFormGroup.value?.samplesCtrl

    if (n_samples_str != null && n_samples_str != undefined){
      const n_samples = parseInt(n_samples_str)

      this._backendService.generate(n_samples).subscribe((data) => {
        
        const blob = new Blob([data], { type: 'application/text-csv' });
        saveAs(blob, "samples.csv");
        
      });

      this._backendService.generate(n_samples)
    }
  }

  onEvaluateClick(){

    this._backendService.evaluate()

    if (this.syntheticData != undefined)
  }
}
