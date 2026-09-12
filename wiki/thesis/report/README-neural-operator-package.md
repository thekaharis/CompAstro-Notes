# Neural-operator report package

This package contains `neural-operator-report.tex`, the main document for the
focused scientific report, and the rendered figures used by it. The report is
written for the default pdfLaTeX compiler on Overleaf or ShareLaTeX.

## Compile

Upload the contents of the accompanying ZIP file to a new project and set
`neural-operator-report.tex` as the main document. Compile with pdfLaTeX. No
external data, Python packages, or local project paths are required.

## Figure manifest

| File | Source |
|---|---|
| `fno_training_trajectories.png` | `_attachments/fno_training_trajectories.png` |
| `mode_weight_profiles_3d.png` | `wiki/thesis/findings/figures/localfno-mode-weights_20260720/mode_weight_profiles_3d.png` |
| `lightcone_grid_3d_validation.png` | `wiki/thesis/findings/figures/archive/ufno-detailed_20260606-234954_job3966888/lightcone_grid_3d_validation.png` |
| `comparison_3d_validation_cone61.png` | Same U-FNO validation figure directory |
| `comparison_3d_validation_cone2322.png` | Same U-FNO validation figure directory |
| `matrix_params_vs_rmse.png` | `_attachments/matrix_params_vs_rmse.png` |
| `matrix_inference_speed_vs_rmse.png` | `_attachments/matrix_inference_speed_vs_rmse.png` |
| `matrix_coherence_vs_bsd_bias.png` | `_attachments/matrix_coherence_vs_bsd_bias.png` |

The figures are copies of the rendered experiment outputs; the source data
and experiment directories are not needed for compilation.
