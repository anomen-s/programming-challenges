package com.example.async.future;

import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;
import com.google.common.util.concurrent.ListeningExecutorService;
import com.google.common.util.concurrent.MoreExecutors;

public class GuavaSample {

    public static void main(String[] args) {
        System.out.println("request received");
        final String uuid = UUID.randomUUID().toString();

        ExecutorService executor = Executors.newFixedThreadPool(10);

        ListeningExecutorService les = MoreExecutors.listeningDecorator(executor);
        final ListenableFuture<String> future = les.submit(() -> saveFile(uuid));

        Futures.addCallback(future, new FutureCallback<>() {
            @Override
            public void onSuccess(String result) {
                System.out.println("success: " + result);
            }

            @Override
            public void onFailure(Throwable t) {
                System.out.println("failed: " + t);
            }
        }, les);

        try {
            final String result = future.get();

            System.out.println("final result: " + result);
        } catch (Exception e) {
            System.out.println("final exception: " + e);
        }
        les.shutdown();
    }

    private static String saveFile(String uuid) {
        try {
            Thread.sleep(1000L);
//            throw new IllegalArgumentException("something fAILED!");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("file saved");
        return "suCCESS for " + uuid;
    }


}
