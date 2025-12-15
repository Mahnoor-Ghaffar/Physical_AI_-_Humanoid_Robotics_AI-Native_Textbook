# Component Contracts: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

This document outlines conceptual contracts (props/interfaces) for custom React components that will be developed to enhance the Docusaurus-based textbook content. These are not traditional API contracts but rather define the expected inputs and behaviors of the interactive components.

## IsaacSimScene Component

**Purpose**: Embed an interactive view or visualization of an Isaac Sim scene within an MDX chapter. This component might display pre-rendered simulations, allow limited interaction with a simulated environment, or visualize USD assets.

**Props**:
-   `src`: `string` (Required) - Path to the Isaac Sim scene asset (e.g., USD file, or a reference to a pre-rendered simulation).
-   `controls`: `boolean` (Optional, Default: `true`) - Whether to display basic viewer controls (zoom, pan, rotate).
-   `width`: `string` (Optional, Default: `100%`) - CSS width property for the component.
-   `height`: `string` (Optional, Default: `400px`) - CSS height property for the component.
-   `interactive`: `boolean` (Optional, Default: `false`) - If `true`, enables advanced user interaction (e.g., selecting objects, running simple actions).
-   `onEvent`: `function` (Optional) - Callback for interactive events within the scene (e.g., `onSelectObject(objectId)`, `onActionTriggered(actionName)`).

**Behavior**:
-   Loads and renders the specified Isaac Sim scene or visualization.
-   Provides basic navigation controls (if `controls` is `true`).
-   Can emit events for user interactions if `interactive` is `true`.

## VslamPipeline Component

**Purpose**: Visualize the different stages or outputs of a VSLAM pipeline, potentially showing real-time (simulated) sensor input, feature extraction, map points, and estimated robot trajectory.

**Props**:
-   `pipelineConfig`: `object` (Required) - Configuration object for the VSLAM pipeline visualization.
    -   `mode`: `enum('live', 'playback', 'static')` (Required) - Determines if the visualization is live (simulated), playback from recorded data, or a static representation.
    -   `dataSrc`: `string` (Conditional, Required if `mode` is `'playback'`) - Path to recorded VSLAM data.
    -   `highlightStage`: `string` (Optional) - Name of a specific stage in the pipeline to highlight (e.g., "FeatureExtraction", "LoopClosure").
-   `width`: `string` (Optional, Default: `100%`) - CSS width property.
-   `height`: `string` (Optional, Default: `400px`) - CSS height property.
-   `showLegend`: `boolean` (Optional, Default: `true`) - Whether to display a legend for visualization elements.

**Behavior**:
-   Renders a visual representation of a VSLAM pipeline.
-   Can animate data flow or robot trajectory based on `mode`.
-   Highlights specific pipeline stages as configured.

## Nav2BehaviorTree Component

**Purpose**: Display and optionally allow exploration of a Nav2 Behavior Tree structure, possibly showing the active path during a simulated navigation task.

**Props**:
-   `btDefinition`: `string` (Required) - XML or equivalent definition of the Nav2 Behavior Tree.
-   `highlightNode`: `string` (Optional) - ID or name of a Behavior Tree node to highlight (e.g., currently active node during simulation playback).
-   `readOnly`: `boolean` (Optional, Default: `true`) - If `false`, allows basic interaction like collapsing/expanding branches.
-   `width`: `string` (Optional, Default: `100%`) - CSS width property.
-   `height`: `string` (Optional, Default: `400px`) - CSS height property.

**Behavior**:
-   Parses and renders the Nav2 Behavior Tree visually.
-   Can highlight specific nodes dynamically.
-   Provides basic interaction for exploring the tree structure.
