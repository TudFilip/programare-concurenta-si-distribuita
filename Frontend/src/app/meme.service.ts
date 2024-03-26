// meme.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Meme } from './meme.model';
import { ɵInternalFormsSharedModule } from '@angular/forms';

@Injectable({
  providedIn: 'root',
})
export class MemeService {
  private apiUrl = 'http://localhost:8081/api/images';

  constructor(private http: HttpClient) {}

  postMeme(file: File): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);
    return this.http.post(this.apiUrl, formData);
  }

  getMeme(): Observable<Meme[]> {
    return this.http.get<Meme[]>(this.apiUrl);
  }
}
