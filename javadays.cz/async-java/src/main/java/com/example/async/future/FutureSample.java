package com.example.async.future;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.stream.IntStream;

public class FutureSample implements Callable<String> {

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        final String uuid = UUID.randomUUID().toString();
        System.out.println("generating UUID:" + uuid);

        final FutureSample futureSample = new FutureSample();
        ExecutorService executor = Executors.newFixedThreadPool(10);

        List<Future<String>> futures = new ArrayList<>();
        IntStream
                .range(0, 10)
                .forEach(i -> futures.add(executor.submit(futureSample)));

        for (Future<String> result : futures) {
            System.out.println("got result: " + result.get());
        }

        executor.shutdown();
    }

    @Override
    public String call() throws Exception {
        Thread.sleep(1000);
        return "sUCCESS";
    }
}
