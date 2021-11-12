package com.example.async.future;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class CompletableFutureChainSample {

    public static void main(String[] args) throws ExecutionException, InterruptedException {


        CompletableFuture<Void> future = CompletableFuture
                .supplyAsync(() -> "request")
                        .thenApplyAsync((String r) -> {
                            System.out.println(r);
                            return "after step 1";
                        })
                .thenApplyAsync( s -> {
                    System.out.println("step 2: " + s);
                    return null;
                });


        future.get();
        System.out.println("final finish");

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
