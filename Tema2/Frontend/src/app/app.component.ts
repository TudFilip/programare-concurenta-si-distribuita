import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Meme } from './meme.model';
import { MemeService } from './meme.service';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'Frontend';
  memes: Meme[] = [];
  
  constructor(private service: MemeService, private sanitizer: DomSanitizer){}

  ngOnInit(): void {
    this.getMemes();
  }

  addMeme(event: any) {
    const file: File = event.target.files[0];
    this.service.postMeme(file).subscribe(
      (response) => {
        console.log('Image uploaded successfully!', response);
        this.memes = [];
        this.getMemes();
      },
      (error) => {
        console.error('Error uploading image:', error);
      }
    )
  }

  createImageFromBlob(image: Blob, meme: Meme): void {
    const reader = new FileReader();
    reader.addEventListener('load', () => {
      meme.img = reader.result as string;
    }, false);

    if (image) {
      reader.readAsDataURL(image);
    }
  }

  //Get all memes ids
  //For each id get the meme
  getMemes() {
    this.service.getMemeIds().subscribe(ids => {
      ids.forEach(id => {
        this.service.getMemeById(id).subscribe(meme => {
          this.service.getDescriptionById(id).subscribe(description => {
            let newMeme: Meme = new Meme();
            this.createImageFromBlob(meme, newMeme);
            newMeme.description = JSON.parse(description).description.slice(',').join(', ');
            newMeme.uuid = "1234";
            this.memes.push(newMeme);
            console.log(this.memes);
          })
          // let newMeme: Meme = new Meme();
          // newMeme.img = "data:image/png;base64," + meme.img;
          // newMeme.description = meme.description;
          // newMeme.uuid = meme.uuid;
          // //newMeme.sentiment = meme.sentiment;
          // this.memes.push(newMeme);
        })
      })
    })
    
  }

  //Old function
  getMeme() {
    this.service.getMeme().subscribe(data => {
      data.forEach(meme => {
        //meme.img = "data:image/png;base64," + meme.img;
        meme.description = meme.description; 
        meme.uuid = meme.uuid;
        // meme.sentiment = meme.sentiment;
        this.memes.push(meme);
      });
      console.log(this.memes);
    })

  }

}
