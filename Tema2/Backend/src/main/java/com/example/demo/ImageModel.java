package com.example.demo;

import java.util.Base64;
import java.util.Objects;

public class ImageModel {
    public Base64 imageData;

    public Base64 getImageData() {
        return imageData;
    }

    public void setImageData(Base64 imageData) {
        this.imageData = imageData;
    }

    public ImageModel(Base64 imageData) {
        this.imageData = imageData;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ImageModel that = (ImageModel) o;
        return Objects.equals(imageData, that.imageData);
    }

    @Override
    public int hashCode() {
        return Objects.hash(imageData);
    }

    @Override
    public String toString() {
        return "ImageModel{" +
                "imageData=" + imageData +
                '}';
    }
}
