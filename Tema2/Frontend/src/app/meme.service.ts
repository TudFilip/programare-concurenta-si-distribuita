// meme.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Meme } from './meme.model';

@Injectable({
  providedIn: 'root'
})
export class MemeService {
  private apiUrl = 'http://localhost:8081/api/memes/meme';

  constructor(private http: HttpClient) {}

  getMemes() : string {
    return '';
  }

  getMeme() : Observable<Meme[]> {
    return this.http.get<Meme[]>(this.apiUrl);
  }
}
