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
import { BackendService } from './services/backend.service';
import {saveAs} from "file-saver";
import {MatSnackBar, MatSnackBarModule} from '@angular/material/snack-bar';

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
    MatSnackBarModule
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

  evaluationFormGroup = this._formBuilderTraining.group({
    evaluationCtrl: ['workclass', Validators.required, ],
  });

  syntheticData: File 
  syntheticDataFileName: string

  realData: File
  realDataFileName: string

  constructor(
    private _formBuilderGeneration: FormBuilder, 
    private _formBuilderTraining: FormBuilder,
    private _backendService: BackendService,
    private _snackBar: MatSnackBar
  ) {}

  openSnackBar(message: string, action: string, config: any) {
    this._snackBar.open(message, action, config);
  }

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
  
    this._backendService.train(this.modelFormGroup.value.modelsCtrl!, this.trainingData!)
      .subscribe((res) => {
        this.openSnackBar("Training completed", "Dismiss", {
          duration: 3000
        })
      }
    );
  }

  onGenerateClick(){

    this._backendService.generate(parseInt(this.samplesFormGroup.value?.samplesCtrl!))
      .subscribe((data: ArrayBuffer) => {
        
        const blob = new Blob([data], { type: 'application/text-csv' });
        saveAs(blob, "samples.csv");
        
      }
    );
  }

  onEvaluateClick(){

    this._backendService.evaluate(this.evaluationFormGroup.value?.evaluationCtrl!, this.syntheticData!, this.realData!)
      .subscribe((data: ArrayBuffer) => {
        const blob = new Blob([data], { type: 'application/pdf' });
        saveAs(blob, "evaluation.pdf");
      }
    );
  }
}
