package com.example;

public class GNodeImpl implements GNode {
    private final String name;
    private final GNode[] children;

    public GNodeImpl(String name, GNode ... children) {
        this.children = children;
        this.name = name;

    }

    public String getName() {
        return this.name;
    }

    public GNode[] getChildren() {
        return this.children;
    }

    @Override
    public String toString() {
        return name;
    }
}
