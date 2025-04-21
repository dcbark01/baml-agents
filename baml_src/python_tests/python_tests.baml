class MyClass {
    @@dynamic
}
function RenderMyClass() -> MyClass {
    client Default
    prompt #"{{ ctx.output_format }}"#
}
