// meme.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Meme } from './meme.model';
import { ɵInternalFormsSharedModule } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class MemeService {
  private apiUrl = 'http://localhost:8081/api/memes/meme';

  constructor(private http: HttpClient) {}

  postMeme(file: File) : Observable<any> {
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);
    console.log(file);
    return this.http.post('http://localhost:8081/images', formData);
  }

  getMemeIds() : Observable<String[]> {
    return this.http.get<String[]>("http://localhost:8081/images");
  }

  getMemeById(id: String) : Observable<Blob> {
    return this.http.get(`http://localhost:8081/images/${id}`, { responseType: 'blob'});
  }

  getDescriptionById(id: String) : Observable<string> {
    return this.http.get(`http://localhost:8081/images/content/${id}`, { responseType: 'text'})
  }

  getMeme() : Observable<Meme[]> {
    return this.http.get<Meme[]>(this.apiUrl);
  }

  // fileToByteArray(file: File): Promise<Uint8Array> {
  //   return new Promise((resolve, reject) => {
  //     const reader = new FileReader();
  //     reader.onload = (event) => {
  //       if (event.target && event.target.result instanceof ArrayBuffer) {
  //         const arrayBuffer = event.target.result;
  //         const byteArray = new Uint8Array(arrayBuffer);
  //         resolve(byteArray);
  //       } else {
  //         reject(new Error("Failed to read file as ArrayBuffer"));
  //       }
  //     };
  //     reader.onerror = (error) => {
  //       reject(error);
  //     };
  //     reader.readAsArrayBuffer(file);
  //   });
  // }
}
