package com.example.async.future;

import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class CompletableFutureSample {

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        final String uuid = UUID.randomUUID().toString();
        System.out.println("generating UUID:" + uuid);


        CompletableFuture<Void> future = CompletableFuture.runAsync(() -> saveFile(uuid));

        future.get();
        System.out.println("finished");

    }

    private static void saveFile(String uuid) {

        try {
            Thread.sleep(1000L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("file saved " + uuid);
    }

}
