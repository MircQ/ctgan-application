// code for product.service.ts

import { Injectable } from '@angular/core';


import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, map } from 'rxjs';

@Injectable({
    providedIn: 'root',
}
)
export class BackendService {

    BASE_URL = "http://localhost:4201"

    constructor(
        private http: HttpClient) { 
        }

    train(model: string, data: File): Observable<Object>{

        var formData = new FormData();

        formData.append('file', data);

        return this.http.post(`${this.BASE_URL}/train/${model}`, formData);
    }

    generate(n_samples: number): Observable<ArrayBuffer>{

        const options: {
            headers?: HttpHeaders;
            observe?: 'body';
            params?: HttpParams;
            reportProgress?: boolean;
            responseType: 'arraybuffer';
            withCredentials?: boolean;
        } = {
            headers: new HttpHeaders({ 
                'Accept':'application/octet-stream',
                'Access-Control-Allow-Origin' : '*'
            }),
            responseType: 'arraybuffer',
            params: new HttpParams().set('samples', n_samples)
        };

        return this.http.get(`${this.BASE_URL}/generate`, options).pipe(
            map((file: ArrayBuffer) => {
                return file;
            })
        );
    }

    evaluate(column_name: string, synthetic_data: File, real_data: File): Observable<ArrayBuffer>{

        var formData = new FormData();

        formData.append('synthetic_data_file', synthetic_data);
        formData.append('real_data_file', real_data);

        const options: {
            headers?: HttpHeaders;
            observe?: 'body';
            params?: HttpParams;
            reportProgress?: boolean;
            responseType: 'arraybuffer';
            withCredentials?: boolean;
        } = {
            headers: new HttpHeaders({ 
                'Accept':'application/pdf',
                'Access-Control-Allow-Origin' : '*'
            }),
            responseType: 'arraybuffer',
            params: new HttpParams().set('column_name', column_name)
        };

        return this.http.post(`${this.BASE_URL}/evaluate`, formData, options).pipe(
            map((file: ArrayBuffer) => {
                return file;
            })
        );;
    }
}