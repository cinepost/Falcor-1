def render_graph_PathTracerGraph():
    g = RenderGraph("PathTracerGraph")
    loadRenderPassLibrary("AccumulatePass.dll")
    loadRenderPassLibrary("GBuffer.dll")
    loadRenderPassLibrary("ToneMapper.dll")
    loadRenderPassLibrary("MegakernelPathTracer.dll")
    AccumulatePass = RenderPass("AccumulatePass", {'enableAccumulation': True})
    g.addPass(AccumulatePass, "AccumulatePass")
    ToneMappingPass = RenderPass("ToneMapper", {'autoExposure': False, 'exposureValue': 0.0})
    g.addPass(ToneMappingPass, "ToneMappingPass")
    GBufferRT = RenderPass("GBufferRT", {'forceCullMode': False, 'cull': CullMode.CullBack, 'samplePattern': SamplePattern.Stratified, 'sampleCount': 16})
    g.addPass(GBufferRT, "GBufferRT")
    MegakernelPathTracer = RenderPass("MegakernelPathTracer", {'mSharedParams': PathTracerParams(useVBuffer=0, useAnalyticLights=0)})
    g.addPass(MegakernelPathTracer, "MegakernelPathTracer")
    g.addEdge("GBufferRT.posW", "MegakernelPathTracer.posW")
    g.addEdge("GBufferRT.normW", "MegakernelPathTracer.normalW")
    g.addEdge("GBufferRT.bitangentW", "MegakernelPathTracer.bitangentW")
    g.addEdge("GBufferRT.faceNormalW", "MegakernelPathTracer.faceNormalW")
    g.addEdge("GBufferRT.viewW", "MegakernelPathTracer.viewW")
    g.addEdge("GBufferRT.diffuseOpacity", "MegakernelPathTracer.mtlDiffOpacity")
    g.addEdge("GBufferRT.specRough", "MegakernelPathTracer.mtlSpecRough")
    g.addEdge("GBufferRT.emissive", "MegakernelPathTracer.mtlEmissive")
    g.addEdge("GBufferRT.matlExtra", "MegakernelPathTracer.mtlParams")
    g.addEdge("MegakernelPathTracer.color", "AccumulatePass.input")
    g.addEdge("AccumulatePass.output", "ToneMappingPass.src")
    g.markOutput("ToneMappingPass.dst")
    return g

PathTracerGraph = render_graph_PathTracerGraph()
try: m.addGraph(PathTracerGraph)
except NameError: None
