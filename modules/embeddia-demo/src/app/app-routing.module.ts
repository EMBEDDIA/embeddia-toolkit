import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CommentAnalyzerComponent} from './comment-analyzer/comment-analyzer.component';
import {ArticleAnalyzerComponent} from './article-analyzer/article-analyzer.component';
import {ArticleGenerationComponent} from './article-generation/article-generation.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {HealthComponent} from './health/health.component';


const routes: Routes = [
  {
    path: 'comment-analyzer',
    pathMatch: 'full',
    component: CommentAnalyzerComponent
  },
  {
    path: 'article-analyzer',
    pathMatch: 'full',
    component: ArticleAnalyzerComponent
  },
  {
    path: 'article-generation',
    pathMatch: 'full',
    component: ArticleGenerationComponent
  },
  {
    path: 'dashboard',
    pathMatch: 'full',
    component: DashboardComponent
  },
  {
    path: '',
    pathMatch: 'full',
    component: HealthComponent
  },
  {
    path: '**',
    redirectTo: ''
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
