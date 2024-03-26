import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Meme } from './meme.model';
import { MemeService } from './meme.service';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  memes: Meme[] = [];

  constructor(private service: MemeService, private sanitizer: DomSanitizer) {}

  ngOnInit(): void {
    this.getAllMemes();
  }

  addMeme(event: any) {
    const file: File = event.target.files[0];
    this.service.postMeme(file).subscribe(
      (response) => {
        console.log('Image uploaded successfully!', response);
        // this.memes = [];
        // this.getMeme();
      },
      (error) => {
        console.error('Error uploading image:', error);
      }
    );
  }

  getAllMemes() {
    this.service.getAllMemes().subscribe((data) => {
      data.forEach((meme) => {
        meme.img = 'data:image/png;base64,' + meme.img;
        meme.description = meme.description;
        meme.uuid = meme.uuid;
        meme.sentiment = meme.sentiment;
        this.memes.push(meme);
      });
      console.log(this.memes);
    });
  }
}
